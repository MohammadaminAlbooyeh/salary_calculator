import './App.css';
import { useState, useMemo } from 'react';

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
      const response = await fetch('http://localhost:5051/calculate', {
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
          <div>
            <label>Bonus (EUR):</label>
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
            <p>Total Net Salary: <strong>€{result['Annual Net Salary (netto annuo)']?.toFixed(2) || result.total_salary || 0}</strong></p>
            <p>Total Tax: <strong>€{result['Total Taxes (tasse totali IRPEF+addiz)']?.toFixed(2) || 'N/A'}</strong></p>
            <p>Tax Rate: <strong>{
              result['Gross Annual Salary (RAL)'] && result['Total Taxes (tasse totali IRPEF+addiz)']
                ? `${((result['Total Taxes (tasse totali IRPEF+addiz)'] / result['Gross Annual Salary (RAL)']) * 100).toFixed(2)}%`
                : 'N/A'
            }</strong></p>
            <p>Monthly Net (12): <strong>€{result['Monthly Net (12 months - 12 mensilità)']?.toFixed(2) || 'N/A'}</strong></p>
            <p>Monthly Net (13): <strong>€{result['Monthly Net (13 months - 13 mensilità)']?.toFixed(2) || 'N/A'}</strong></p>
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
