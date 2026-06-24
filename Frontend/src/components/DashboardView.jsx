import React, { useState, useEffect } from 'react';

export default function DashboardView({ initialData }) {
  const hasPricing = initialData.pricing && initialData.pricing.length > 0;
  const hasChurn = initialData.churn && initialData.churn.length > 0;

  const [activeTab, setActiveTab] = useState('pricing');
  const [pricingRows, setPricingRows] = useState(initialData.pricing);
  const [churnRows, setChurnRows] = useState(initialData.churn);
  
  // Track which specific rows have been successfully committed to the system
  const [appliedPrices, setAppliedPrices] = useState({});
  const [automationState, setAutomationState] = useState({});

  useEffect(() => {
    if (!hasPricing && hasChurn) {
      setActiveTab('churn');
    }
  }, [hasPricing, hasChurn]);

  const toggleAutomation = (id) => {
    setAutomationState(prev => ({ ...prev, [id]: !prev[id] }));
  };

  // Upgraded Professional Action Handler
  const handleApplyPrice = (id, recommendedPrice) => {
    // 1. Instantly update the data array so Base Price reflects the new reality
    setPricingRows(prevRows => 
      prevRows.map(row => 
        row.id === id ? { ...row, base_price: recommendedPrice } : row
      )
    );

    // 2. Lock the applied state configuration for this row item to trigger our UI morph
    setAppliedPrices(prev => ({ ...prev, [id]: true }));
  };

  const dispatchRetentionOffer = (customerId) => {
    alert(`[Retention Shield Injected] Dispatched customized transactional mitigation coupon matrices directly to node ${customerId}`);
    setChurnRows(prev => prev.filter(c => c.customer_id !== customerId));
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex">
      {/* Sidebar Layout */}
      <aside className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col p-6">
        <div className="mb-8">
          <h2 className="text-xl font-black uppercase tracking-wider bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
            Shield Core v1.2
          </h2>
          <p className="text-xs text-slate-500 font-mono mt-1">Mode: {hasPricing && hasChurn ? "Omni-Channel" : "Single Module"}</p>
        </div>

        <nav className="space-y-2 flex-1">
          {hasPricing && (
            <button
              onClick={() => setActiveTab('pricing')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-all text-sm ${
                activeTab === 'pricing' ? 'bg-cyan-500/10 text-cyan-400 border border-cyan-500/30' : 'text-slate-400 hover:bg-slate-800'
              }`}
            >
              <span>📊 Dynamic Price Optimizer</span>
            </button>
          )}
          
          {hasChurn && (
            <button
              onClick={() => setActiveTab('churn')}
              className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl font-medium transition-all text-sm ${
                activeTab === 'churn' ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30' : 'text-slate-400 hover:bg-slate-800'
              }`}
            >
              <span>🛡️ Customer Churn Shield</span>
            </button>
          )}
        </nav>
      </aside>

      {/* Main Terminal Metric Canvas */}
      <main className="flex-1 p-10 overflow-y-auto">
        {activeTab === 'pricing' && hasPricing ? (
          <div>
            <div className="mb-6">
              <h1 className="text-2xl font-bold tracking-tight">Dynamic Pricing Optimization Terminal</h1>
              <p className="text-sm text-slate-400">Real-time target evaluations running elastic regression pipelines against active catalog constraints.</p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-800/50 border-b border-slate-800 text-xs font-mono text-slate-400 uppercase tracking-wider">
                    <th className="p-4">SKU Index</th>
                    <th className="p-4">Catalog Item Name</th>
                    <th className="p-4 text-center">Stock Level</th>
                    <th className="p-4 text-right">Base Config</th>
                    <th className="p-4 text-right">Competitor Index</th>
                    <th className="p-4 text-right text-cyan-400">AI Recommendation</th>
                    <th className="p-4 text-center">Automated Engine</th>
                    <th className="p-4 text-center">Execution Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 text-sm">
                  {pricingRows.map((row, idx) => {
                    const currentRowId = row.id || `SKU-${1000 + idx}`;
                    const isApplied = !!appliedPrices[currentRowId];

                    return (
                      <tr key={currentRowId} className="hover:bg-slate-800/30 transition-colors">
                        <td className="p-4 font-mono text-xs text-slate-400">{currentRowId}</td>
                        <td className="p-4 font-medium text-slate-200">{row.name || "Catalog Product Item"}</td>
                        <td className="p-4 text-center">
                          <span className="px-2 py-1 rounded text-xs font-mono font-bold bg-slate-800 text-slate-300">
                            {row.stock_level ?? 45} pcs
                          </span>
                        </td>
                        <td className="p-4 text-right font-mono transition-all duration-300">
                          <span className={isApplied ? "text-emerald-400 font-bold" : "text-slate-100"}>
                            ${(row.base_price).toFixed(2)}
                          </span>
                        </td>
                        <td className="p-4 text-right font-mono text-slate-400">${(row.competitor_price ?? row.base_price).toFixed(2)}</td>
                        <td className="p-4 text-right font-mono font-bold text-cyan-400 text-base">${(row.recommended_price || row.base_price).toFixed(2)}</td>
                        <td className="p-4 text-center">
                          <label className="relative inline-flex items-center cursor-pointer justify-center">
                            <input type="checkbox" checked={!!automationState[currentRowId]} onChange={() => toggleAutomation(currentRowId)} className="sr-only peer" />
                            <div className="w-9 h-5 bg-slate-700 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-slate-300 after:border-slate-300 after:border after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-cyan-500"></div>
                          </label>
                        </td>
                        <td className="p-4 text-center">
                          {isApplied ? (
                            /* State 2: Grayed-out, disabled button with green checkmark vector */
                            <button
                              disabled
                              className="inline-flex items-center space-x-1.5 px-4 py-1.5 bg-slate-800/80 text-slate-500 border border-slate-700/60 rounded-lg text-xs font-semibold cursor-not-allowed transition-all"
                            >
                              <svg className="w-4 h-4 text-emerald-500" fill="none" stroke="currentColor" strokeWidth="2.5" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                              </svg>
                              <span>Applied</span>
                            </button>
                          ) : (
                            /* State 1: Active, vibrant action trigger element */
                            <button
                              onClick={() => handleApplyPrice(currentRowId, row.recommended_price || row.base_price)}
                              className="px-4 py-1.5 bg-cyan-600 hover:bg-cyan-500 active:scale-95 text-white font-semibold rounded-lg text-xs shadow-md hover:shadow-cyan-600/10 transition-all"
                            >
                              Apply
                            </button>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        ) : (
          <div>
            <div className="mb-6">
              <h1 className="text-2xl font-bold tracking-tight">Customer Churn Retention Shield</h1>
              <p className="text-sm text-slate-400">Proactively tracking classification matrices highlighting users running structural risks of platform defection.</p>
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden shadow-xl">
              <table className="w-full text-left border-collapse">
                <thead>
                  <tr className="bg-slate-800/50 border-b border-slate-800 text-xs font-mono text-slate-400 uppercase tracking-wider">
                    <th className="p-4">Customer ID</th>
                    <th className="p-4 text-center">Logins / Month</th>
                    <th className="p-4 text-center">Purchase Stagnancy</th>
                    <th className="p-4 text-center">Cart Abandonment</th>
                    <th className="p-4 text-right text-rose-400">Risk Probability</th>
                    <th className="p-4 text-center">Mitigation Dispatch</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800 text-sm">
                  {churnRows.map((row, idx) => {
                    const currentCustId = row.customer_id || `USR-${9000 + idx}`;
                    const isHighRisk = row.churn_probability > 0.75;
                    return (
                      <tr key={currentCustId} className="hover:bg-slate-800/30 transition-colors">
                        <td className="p-4 font-mono text-xs text-slate-400">{currentCustId}</td>
                        <td className="p-4 text-center font-mono">{row.login_frequency}</td>
                        <td className="p-4 text-center font-mono text-slate-300">{row.days_since_last_purchase} days ago</td>
                        <td className="p-4 text-center font-mono text-slate-400">{(row.cart_abandonment_rate * 100).toFixed(0)}%</td>
                        <td className="p-4 text-right">
                          <span className={`inline-block font-mono font-bold text-base px-2 py-0.5 rounded ${
                            isHighRisk ? 'text-rose-400 bg-rose-950/60 border border-rose-800/80' : 'text-emerald-400'
                          }`}>
                            {(row.churn_probability * 100).toFixed(1)}%
                          </span>
                        </td>
                        <td className="p-4 text-center">
                          <button
                            onClick={() => dispatchRetentionOffer(currentCustId)}
                            className="px-3 py-1.5 bg-gradient-to-r from-rose-600 to-orange-600 hover:from-rose-500 hover:to-orange-500 text-white font-semibold rounded-lg text-xs shadow-md transition-all"
                          >
                            Send Offer
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}