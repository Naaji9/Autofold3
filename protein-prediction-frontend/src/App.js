import React from 'react';
import './App.css';
import ProteinPredictionForm from './components/ProteinPredictionForm';
import Footer from './components/Footer'; 
import logo from './assets/Logo.png';
import logo1 from './assets/Logo1.png';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <div>
          <img src={logo} alt="Logo" className="App-logo" />
          <img src={logo1} alt="Logo1" className="App-logo1" />
        </div>
        <h1>Protein Prediction Automation</h1>
        <p className="p">Automate your protein structure predictions effortlessly</p>
      </header>
      <main className='App-main'>
        <ProteinPredictionForm />
      </main>
      <Footer /> {/* add the footer here */}
    </div>
  );
}

export default App;