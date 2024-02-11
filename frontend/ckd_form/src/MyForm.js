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
      <label>
        Packed Cell Volume:
        <input
          type="number"
          name="packedCellVolume"
          value={formData.packedCellVolume}
          onChange={handleChange}
        />
      </label>
      <label>
        Serum Creatinine:
        <input
          type="number"
          name="serumCreatinine"
          value={formData.serumCreatinine}
          onChange={handleChange}
        />
      </label>
      <label>
        Sodium:
        <input
          type="number"
          name="sodium"
          value={formData.sodium}
          onChange={handleChange}
        />
      </label>
      <label>
        Potassium:
        <input
          type="number"
          name="potassium"
          value={formData.potassium}
          onChange={handleChange}
        />
      </label>
      <label>
        Hemoglobin:
        <input
          type="number"
          name="hemoglobin"
          value={formData.hemoglobin}
          onChange={handleChange}
        />
      </label>
      <label>
        Red Blood Cells:
        <select name="redBloodCells" value={formData.redBloodCells} onChange={handleChange}>
          <option value="normal">Normal</option>
          <option value="abnormal">Abnormal</option>
        </select>
      </label>
      <label>
        Coronary Artery Disease:
        <select
          name="coronaryArteryDisease"
          value={formData.coronaryArteryDisease}
          onChange={handleChange}
        >
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <label>
        Appetite:
        <select name="appetite" value={formData.appetite} onChange={handleChange}>
          <option value="good">Good</option>
          <option value="poor">Poor</option>
        </select>
      </label>
      <label>
        Hypertension:
        <select name="hypertension" value={formData.hypertension} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <label>
        Diabetes:
        <select name="diabetes" value={formData.diabetes} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <label>
        Anemia:
        <select name="anemia" value={formData.anemia} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <label>
        Pedal Edema:
        <select name="pedalEdema" value={formData.pedalEdema} onChange={handleChange}>
          <option value="yes">Yes</option>
          <option value="no">No</option>
        </select>
      </label>
      <button type="submit">Submit</button>
    </form>
  );
};

export default MyForm;
