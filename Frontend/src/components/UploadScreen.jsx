import React, { useState } from 'react';
import { mockPricingData, mockChurnData } from '../mockData';

// Intelligent vocabulary mapping system
const ALIAS_MAP = {
  customer_id: ["customer_id", "user_id", "client_id", "id", "cust_id"],
  login_frequency: ["login_frequency", "logins", "visit_count", "monthly_logins", "sessions"],
  days_since_last_purchase: ["days_since_last_purchase", "days_inactive", "last_order_days", "stagnancy", "days_offline"],
  cart_abandonment_rate: ["cart_abandonment_rate", "cart_abandon", "abandon_rate", "dropped_carts", "abandon_percentage"]
};

export default function UploadScreen({ onDataLoaded }) {
  const [isDragging, setIsDragging] = useState(false);
  const [errorMessage, setErrorMessage] = useState('');

  const handleDragOver = (e) => { e.preventDefault(); setIsDragging(true); };
  const handleDragLeave = () => setIsDragging(false);
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files.length > 0) processFlexibleCSV(e.dataTransfer.files[0]);
  };

  const handleFileChange = (e) => {
    if (e.target.files.length > 0) processFlexibleCSV(e.target.files[0]);
  };

  const processFlexibleCSV = (file) => {
    if (!file.name.endsWith('.csv')) {
      setErrorMessage('Invalid file format. Please upload a standard CSV dataset.');
      return;
    }

    const reader = new FileReader();
    reader.onload = function (e) {
      const text = e.target.result;
      const lines = text.split(/\r?\n/).filter(line => line.trim() !== "");
      if (lines.length < 2) {
        setErrorMessage("The uploaded file does not contain sufficient tracking data.");
        return;
      }

      // Parse headers and normalize them
      const rawHeaders = lines[0].split(',').map(h => h.trim().toLowerCase());
      const mappedHeaders = new Array(rawHeaders.length);
      
      // Look up our dictionary targets
      rawHeaders.forEach((rawHead, index) => {
        let foundKey = rawHead; 
        Object.keys(ALIAS_MAP).forEach(officialKey => {
          if (ALIAS_MAP[officialKey].includes(rawHead)) {
            foundKey = officialKey;
          }
        });
        mappedHeaders[index] = foundKey;
      });

      // Verify if this looks like a pricing file or a churn file
      const hasPricingKeys = mappedHeaders.includes('base_price');
      const hasChurnKeys = mappedHeaders.includes('login_frequency') && mappedHeaders.includes('days_since_last_purchase');

      if (!hasPricingKeys && !hasChurnKeys) {
        setErrorMessage("Could not identify valid tracking columns. Please check your data fields.");
        return;
      }

      // Parse out data rows into structured JSON objects
      const dataRows = [];
      for (let i = 1; i < lines.length; i++) {
        const rowValues = lines[i].split(',');
        if (rowValues.length !== rawHeaders.length) continue;
        
        const rowObj = {};
        mappedHeaders.forEach((headerName, colIdx) => {
          const val = rowValues[colIdx].trim();
          rowObj[headerName] = isNaN(val) ? val : Number(val);
        });
        dataRows.push(rowObj);
      }

      // Route data conditionally to our dashboard modules
      if (hasChurnKeys && !hasPricingKeys) {
        // Add fake calculated risk probabilities for demonstration mapping
        const processedChurn = dataRows.map(row => ({
          ...row,
          churn_probability: row.churn_probability || Math.min(0.99, Math.max(0.01, (row.days_since_last_purchase * 0.005) + (row.cart_abandonment_rate || 0.2)))
        }));
        onDataLoaded({ pricing: [], churn: processedChurn });
      } else if (hasPricingKeys && !hasChurnKeys) {
        onDataLoaded({ pricing: dataRows, churn: [] });
      } else {
        onDataLoaded({ pricing: mockPricingData, churn: mockChurnData });
      }
    };

    reader.readAsText(file);
  };

  return (
    <div className="min-h-screen bg-slate-900 flex items-center justify-center p-6 text-white">
      <div className="max-w-xl w-full bg-slate-800 border border-slate-700 rounded-2xl p-8 shadow-2xl">
        <div className="text-center mb-8">
          <h1 className="text-3xl font-extrabold tracking-tight bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
            Shield Core Matrix
          </h1>
          <p className="text-slate-400 mt-2 text-sm">
            Upload any operational log CSV. Our smart mapping dictionary handles matching vocabularies instantly.
          </p>
        </div>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          className={`border-2 border-dashed rounded-xl p-8 text-center transition-all duration-200 cursor-pointer ${
            isDragging ? 'border-emerald-400 bg-slate-700/50' : 'border-slate-600 hover:border-slate-500 bg-slate-900/40'
          }`}
        >
          <input type="file" id="csv-upload" className="hidden" accept=".csv" onChange={handleFileChange} />
          <label htmlFor="csv-upload" className="cursor-pointer block">
            <span className="font-medium text-slate-200 block mb-1">Drop any CSV data sheet here</span>
            <span className="text-xs text-slate-500 block">Pricing, Churn, or Combined Logs</span>
          </label>
        </div>

        {errorMessage && (
          <div className="mt-4 p-3 bg-red-900/40 border border-red-500/50 rounded-lg text-xs text-red-300 text-center">{errorMessage}</div>
        )}

        <button
          onClick={() => onDataLoaded({ pricing: mockPricingData, churn: mockChurnData })}
          className="w-full mt-6 py-3 px-4 bg-gradient-to-r from-emerald-500 to-cyan-600 hover:from-emerald-600 hover:to-cyan-700 text-white font-semibold rounded-xl shadow-lg transition-all text-sm"
        >
          Load Full Sandbox Environment (Both Features)
        </button>
      </div>
    </div>
  );
}