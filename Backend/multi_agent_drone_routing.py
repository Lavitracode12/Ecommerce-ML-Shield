# Start of HEAD
import json
import sys
import math

input_data = json.loads(sys.stdin.read())

map_size = input_data['map_size']
warehouse = [map_size[0] / 2, map_size[1] / 2]
drones = input_data['drones']
deliveries = input_data['deliveries']
no_fly_zones = input_data.get('no_fly_zones', [])
charging_stations = input_data.get('charging_stations', [])
# End of HEAD

# Start of BODY
def solve(warehouse, drones, deliveries, no_fly_zones, charging_stations):
    def dist(p1, p2):
        return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

    def is_inside_nfz(x, y, t, nfz):
        if not (nfz['T_start'] <= t <= nfz['T_end']):
            return False
        if nfz['shape'] == 'circle':
            cx, cy = nfz['center']
            r = nfz['radius']
            return ((x - cx)**2 + (y - cy)**2) <= (r**2 + 1e-3)
        elif nfz['shape'] == 'rectangle':
            (x1, y1), (x2, y2) = nfz['corners']
            x_min, x_max = min(x1, x2), max(x1, x2)
            y_min, y_max = min(y1, y2), max(y1, y2)
            return (x_min - 1e-3 <= x <= x_max + 1e-3) and (y_min - 1e-3 <= y <= y_max + 1e-3)
        return False

    def check_segment_collision(p1, p2, t_start):
        d = dist(p1, p2)
        if d < 1e-3:
            return False, t_start
        # Fast sampling to prevent timeouts
        steps = min(50, max(10, int(d / 2)))
        for i in range(steps + 1):
            alpha = i / steps
            curr_x = p1[0] + alpha * (p2[0] - p1[0])
            curr_y = p1[1] + alpha * (p2[1] - p1[1])
            curr_t = t_start + alpha * d
            for nfz in no_fly_zones:
                if is_inside_nfz(curr_x, curr_y, curr_t, nfz):
                    return True, nfz['T_end'] + 0.1
        return False, t_start

    def plan_safe_leg(p1, p2, t_start):
        blocked, wait_until = check_segment_collision(p1, p2, t_start)
        if not blocked:
            return [{'x': p2[0], 'y': p2[1], 'duration': dist(p1, p2), 'action': 'WAYPOINT'}]
        
        # Strategy 1: Instant mathematical wait calculation
        blocked_after_wait, _ = check_segment_collision(p1, p2, wait_until)
        if not blocked_after_wait:
            return [
                {'x': p1[0], 'y': p1[1], 'duration': wait_until - t_start, 'action': 'WAIT'},
                {'x': p2[0], 'y': p2[1], 'duration': dist(p1, p2), 'action': 'WAYPOINT'}
            ]
            
        # Strategy 2: Fast 4-point geometric bypass bounding box
        offsets = [25, -25, 50, -50]
        for offset in offsets:
            mx = (p1[0] + p2[0]) / 2.0 + offset
            my = (p1[1] + p2[1]) / 2.0 + offset
            mx = max(0, min(map_size[0], mx))
            my = max(0, min(map_size[1], my))
            
            b1, _ = check_segment_collision(p1, [mx, my], t_start)
            if not b1:
                t_mid = t_start + dist(p1, [mx, my])
                b2, _ = check_segment_collision([mx, my], p2, t_mid)
                if not b2:
                    return [
                        {'x': mx, 'y': my, 'duration': dist(p1, [mx, my]), 'action': 'WAYPOINT'},
                        {'x': p2[0], 'y': p2[1], 'duration': dist([mx, my], p2), 'action': 'WAYPOINT'}
                    ]
                    
        return [{'x': p2[0], 'y': p2[1], 'duration': dist(p1, p2), 'action': 'WAYPOINT'}]

    flight_manifest = []
    undelivered = sorted(deliveries, key=lambda d: d['deadline'])

    for drone in drones:
        if not undelivered:
            break
            
        max_payload = drone['max_payload']
        drone_manifest_path = []
        curr_pos = [warehouse[0], warehouse[1]]
        curr_time = 0.0
        curr_battery = 500.0
        
        while undelivered:
            batch = []
            curr_weight = 0.0
            idx = 0
            
            while idx < len(undelivered):
                d_item = undelivered[idx]
                if curr_weight + d_item['weight'] <= max_payload:
                    batch.append(d_item)
                    curr_weight += d_item['weight']
                    undelivered.pop(idx)
                else:
                    idx += 1
                    
            if not batch:
                break
                
            # Document PICKUP event sequence
            drone_manifest_path.append({
                "x": warehouse[0], "y": warehouse[1],
                "t": curr_time, "action": "PICKUP",
                "delivery_ids": [b['id'] for b in batch]
            })
            
            batch_sorted = sorted(batch, key=lambda b: b['weight'], reverse=True)
            active_payload = curr_weight
            trip_valid = True
            temp_legs = []
            
            for target in batch_sorted:
                target_pos = [target['x'], target['y']]
                legs = plan_safe_leg(curr_pos, target_pos, curr_time)
                
                for leg in legs:
                    duration = leg['duration']
                    if leg['action'] == 'WAIT':
                        # Valid WAIT structure: same coordinates, advanced time
                        curr_time += duration
                        temp_legs.append({"x": curr_pos[0], "y": curr_pos[1], "t": curr_time, "action": "WAIT"})
                    else:
                        energy_spent = duration * (1.0 + active_payload)
                        curr_battery -= energy_spent
                        curr_time += duration
                        temp_legs.append({"x": leg['x'], "y": leg['y'], "t": curr_time, "action": "WAYPOINT"})
                        curr_pos = [leg['x'], leg['y']]
                
                if temp_legs and temp_legs[-1]["action"] == "WAYPOINT":
                    temp_legs[-1]["action"] = "DELIVER"
                    temp_legs[-1]["delivery_id"] = target['id']
                    temp_legs[-1]["x"] = target_pos[0]
                    temp_legs[-1]["y"] = target_pos[1]
                    curr_pos = target_pos
                    
                if curr_time > target['deadline'] or curr_battery < 0:
                    trip_valid = False
                    break
                    
                active_payload -= target['weight']
                
            if trip_valid:
                home_legs = plan_safe_leg(curr_pos, warehouse, curr_time)
                total_home_dist = sum([hl['duration'] for hl in home_legs if hl['action'] == 'WAYPOINT'])
                
                # Check mid-trip charging station diversion
                if curr_battery < total_home_dist and charging_stations:
                    station = min(charging_stations, key=lambda cs: dist(curr_pos, [cs['x'], cs['y']]))
                    cs_pos = [station['x'], station['y']]
                    
                    cs_legs = plan_safe_leg(curr_pos, cs_pos, curr_time)
                    for cl in cs_legs:
                        duration = cl['duration']
                        if cl['action'] == 'WAIT':
                            curr_time += duration
                            temp_legs.append({"x": curr_pos[0], "y": curr_pos[1], "t": curr_time, "action": "WAIT"})
                        else:
                            curr_battery -= duration * 1.0
                            curr_time += duration
                            temp_legs.append({"x": cl['x'], "y": cl['y'], "t": curr_time, "action": "WAYPOINT"})
                            curr_pos = [cl['x'], cl['y']]
                            
                    if temp_legs and temp_legs[-1]["action"] == "WAYPOINT":
                        temp_legs[-1]["x"] = cs_pos[0]
                        temp_legs[-1]["y"] = cs_pos[1]
                        curr_pos = cs_pos
                        
                    temp_legs.append({"x": curr_pos[0], "y": curr_pos[1], "t": curr_time, "action": "CHARGE"})
                    
                    energy_needed = 500.0 - curr_battery
                    charge_time = energy_needed / 2.0
                    curr_time += charge_time
                    curr_battery = 500.0
                    
                    temp_legs.append({"x": curr_pos[0], "y": curr_pos[1], "t": curr_time, "action": "CHARGE_COMPLETE"})
                    home_legs = plan_safe_leg(curr_pos, warehouse, curr_time)

                for hl in home_legs:
                    duration = hl['duration']
                    if hl['action'] == 'WAIT':
                        curr_time += duration
                        temp_legs.append({"x": curr_pos[0], "y": curr_pos[1], "t": curr_time, "action": "WAIT"})
                    else:
                        curr_battery -= duration * 1.0
                        curr_time += duration
                        temp_legs.append({"x": hl['x'], "y": hl['y'], "t": curr_time, "action": "WAYPOINT"})
                        curr_pos = [hl['x'], hl['y']]
                        
                if temp_legs and temp_legs[-1]["action"] == "WAYPOINT":
                    temp_legs[-1]["action"] = "RETURN"
                    temp_legs[-1]["x"] = warehouse[0]
                    temp_legs[-1]["y"] = warehouse[1]
                else:
                    temp_legs.append({"x": warehouse[0], "y": warehouse[1], "t": curr_time, "action": "RETURN"})
                    
                drone_manifest_path.extend(temp_legs)
                curr_pos = [warehouse[0], warehouse[1]]
                curr_battery = 500.0  # Automatic full recharge at warehouse base
            else:
                undelivered.extend(batch)
                undelivered = sorted(undelivered, key=lambda d: d['deadline'])
                break

        if len(drone_manifest_path) > 1:
            flight_manifest.append({
                "drone_id": drone['id'],
                "path": drone_manifest_path
            })

    return flight_manifest
# End of BODY

# Start of TAIL
result = solve(warehouse, drones, deliveries, no_fly_zones, charging_stations)
output = {"flight_manifest": result}
print(json.dumps(output))
# End of TAIL