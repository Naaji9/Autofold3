import React, { useState } from 'react';
import './ProteinPredictionForm.css';
import './global.css';
import structureGif from '../assets/structure.gif';  // Path to your GIF

function ProteinPredictionForm() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [file, setFile] = useState(null);
    const [status, setStatus] = useState('');

    const handleSubmit = async (e) => {
        e.preventDefault();
        setStatus('Uploading file...');

        const formData = new FormData();
        formData.append('email', email);
        formData.append('password', password);
        formData.append('file', file);

        try {
            setStatus('Submitting data to server...');
            await new Promise(resolve => setTimeout(resolve, 1000));

            const response = await fetch('http://127.0.0.1:8000/api/submit-dataset/', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                setStatus('Automation started... processing...');
                await new Promise(resolve => setTimeout(resolve, 2000));
                setStatus('Downloading results...');
                await new Promise(resolve => setTimeout(resolve, 2000));

                const result = await response.json();
                setStatus(result.message || 'Process completed successfully!');
            } else {
                setStatus('Error: Unable to process your request.');
            }
        } catch (error) {
            setStatus('Error: Unable to connect to server.');
        }
    };

    return (
        <div className="form-and-gif-container">
            <div className="form-container">
            <h2 className="alpha">Alphafold 3</h2>
                <form onSubmit={handleSubmit} className="prediction-form">
                    <label>Email:</label>
                    <input
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        placeholder="Enter your Gmail"
                        required
                    />
                    <label>Password:</label>
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        placeholder="Enter your password"
                        required
                    />
                    <label>Upload File:</label>
                    <input
                        type="file"
                        onChange={(e) => setFile(e.target.files[0])}
                        accept=".xlsx"
                        required
                    />
                     <span className="tooltip-text">Upload Excel file with variant, mutation, and fasta_sequence</span>
                    <button type="submit">Submit</button>
                </form>
                {status && <p className="status-message">{status}</p>}
            </div>
            <div className="gif-container">
            <h2 className="alpha1">Example Alphafold Protein Structure  3D </h2>
                <img src={structureGif} alt="3D Structure" className="structure-gif" />
            </div>
        </div>
    );
}

export default ProteinPredictionForm;
