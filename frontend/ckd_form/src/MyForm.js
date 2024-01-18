// MyForm.js
import React, { useState } from 'react';

const MyForm = () => {
  const [formData, setFormData] = useState({
    age: 0,
    bloodPressure: 0,
    redBloodCellCount: 0,
    whiteBloodCellCount: 0,
    packedCellVolume: 0,
    serumCreatinine: 0,
    sodium: 0,
    potassium: 0,
    hemoglobin: 0,
    redBloodCells: 'normal',
    coronaryArteryDisease: 'yes',
    appetite: 'good',
    hypertension: 'yes',
    diabetes: 'yes',
    anemia: 'yes',
    pedalEdema: 'yes',
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // Make a POST request using fetch or a library like axios
      const response = await fetch('http://localhost:80/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Add any other headers as needed
        },
        body: JSON.stringify(formData),
      });

      // Handle the response, e.g., show success message or redirect
      console.log('Response:', response);
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Age:
        <input type="number" name="age" value={formData.age} onChange={handleChange} />
      </label>
      <label>
        Blood Pressure (mm/HG):
        <input
          type="number"
          name="bloodPressure"
          value={formData.bloodPressure}
          onChange={handleChange}
        />
      </label>
      <label>
        Red Blood Cell Count:
        <input
          type="number"
          name="redBloodCellCount"
          value={formData.redBloodCellCount}
          onChange={handleChange}
        />
      </label>
      <label>
        White Blood Cell Count:
        <input
          type="number"
          name="whiteBloodCellCount"
          value={formData.whiteBloodCellCount}
          onChange={handleChange}
        />
      </label>

      {/* Add other form fields based on the provided questions... */}

      <button type="submit">Submit</button>
    </form>
  );
};

export default MyForm;
