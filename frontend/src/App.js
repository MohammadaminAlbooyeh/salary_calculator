import './App.css';
import { useState } from 'react';

function App() {
  const [salary, setSalary] = useState('');
  const [bonus, setBonus] = useState('');
  const [deductions, setDeductions] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [validation, setValidation] = useState({});

  const appClass = 'App dark-theme';

  const handleRecalculate = () => {
    const fakeEvent = { preventDefault: () => {} };
    handleSubmit(fakeEvent);
  };

  const validateForm = () => {
    const errors = {};
    if (!salary || Number(salary) <= 0) {
      errors.salary = 'Gross salary must be > 0';
    }
    return errors;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const errors = validateForm();
    setValidation(errors);
    if (Object.keys(errors).length > 0) {
      return;
    }
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await fetch('http://56.228.42.29:5051/calculate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          base_salary: Number(salary),
          bonus: Number(bonus),
          deductions: Number(deductions),
        }),
      });
      if (!response.ok) {
        throw new Error('API error');
      }
      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError('Failed to fetch result.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={appClass}>
      <header className="App-header">
        <h1>💶 Salary Calculator (Italy-2025)</h1>
        <form onSubmit={handleSubmit}>
          <div className="field">
            <label>Gross annual salary (EUR): <span className="tooltip">?<span className="tooltip-text">Base salary before taxes and deductions</span></span></label>
            <input type="number" value={salary} onChange={e => setSalary(e.target.value)} required placeholder="e.g. 50000" />
            {validation.salary && <div className="validation-error">{validation.salary}</div>}
          </div>
          <div className="field">
            <label>Bonus (EUR): <span className="tooltip">?<span className="tooltip-text">Any additional income value</span></span></label>
            <input type="number" value={bonus} onChange={e => setBonus(e.target.value)} placeholder="e.g. 5000" />
          </div>
          <div className="field">
            <label>Deductions (EUR): <span className="tooltip">?<span className="tooltip-text">Costs and amounts to subtract</span></span></label>
            <input type="number" value={deductions} onChange={e => setDeductions(e.target.value)} placeholder="e.g. 2000" />
          </div>
          <div className="button-group">
            <button type="submit" disabled={loading}>Calculate My Salary</button>
            <button type="button" onClick={handleRecalculate} disabled={loading}>Recalculate</button>
          </div>
        </form>
        {loading && <p>Calculating...</p>}
        {error && <div className="error">{error}</div>}
        {result && (
          <div className="result-container">
            <h2>Result</h2>
            <div className="result-grid">
              <div className="result-item large-font large-label">
                <span className="result-label">Monthly Net (12)</span>
                <span className="result-value">€{result['Monthly Net (12 months - 12 mensilità)']?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="result-item large-font large-label">
                <span className="result-label">Monthly Net (13)</span>
                <span className="result-value">€{result['Monthly Net (13 months - 13 mensilità)']?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Annual Net Salary</span>
                <span className="result-value">€{result['Annual Net Salary (netto annuo)']?.toFixed(2) || result.total_salary || 0}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Total Taxes</span>
                <span className="result-value">€{result['Total Taxes (tasse totali IRPEF+addiz)']?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Effective Total Tax Rate</span>
                <span className="result-value">{result['Effective Total Tax Rate (%)']?.toFixed(2) || 'N/A'}%</span>
              </div>
            </div>
            <h3>Tax Breakdown</h3>
            <div className="result-grid">
              <div className="result-item">
                <span className="result-label">IRPEF</span>
                <span className="result-value">€{result['Net IRPEF (IRPEF netta)']?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Addizionale Regionale</span>
                <span className="result-value">€{result['Addizionale Regionale']?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Addizionale Comunale</span>
                <span className="result-value">€{result['Addizionale Comunale']?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="result-item">
                <span className="result-label">INPS (Employee)</span>
                <span className="result-value">€{result['INPS Contributions (contributi INPS)']?.toFixed(2) || 'N/A'}</span>
              </div>
            </div>
            <h3>Pension Contributions</h3>
            <div className="result-grid">
              <div className="result-item">
                <span className="result-label">Employee Share</span>
                <span className="result-value">€{result['INPS Contributions (contributi INPS)']?.toFixed(2) || 'N/A'}</span>
              </div>
              <div className="result-item">
                <span className="result-label">Employer Share</span>
                <span className="result-value">€{result['Employer INPS Share (quota datore)']?.toFixed(2) || 'N/A'}</span>
              </div>
            </div>
          </div>
        )}
        <div className="footer">
          © 2025 Italy Salary Calculator | For informational purposes only
        </div>
      </header>
    </div>
  );
}

export default App;
