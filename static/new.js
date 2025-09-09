function submitForm() {
    // Get form values
    const name = document.getElementById('name').value;
    const patientId = document.getElementById('patientId').value;
    
    // Get feature values
    const defaultFeatures = {
        radius_mean: parseFloat(document.getElementById('radius_mean').value),
        texture_mean: parseFloat(document.getElementById('texture_mean').value),
        perimeter_mean: parseFloat(document.getElementById('perimeter_mean').value),
        area_mean: parseFloat(document.getElementById('area_mean').value),
        smoothness_mean: parseFloat(document.getElementById('smoothness_mean').value),
        compactness_mean: parseFloat(document.getElementById('compactness_mean').value),
        concavity_mean: parseFloat(document.getElementById('concavity_mean').value),
        concave_points_mean: parseFloat(document.getElementById('concave_points_mean').value),
        symmetry_mean: parseFloat(document.getElementById('symmetry_mean').value),
        fractal_dimension_mean: parseFloat(document.getElementById('fractal_dimension_mean').value),
        radius_se: parseFloat(document.getElementById('radius_se').value),
        texture_se: parseFloat(document.getElementById('texture_se').value),
        perimeter_se: parseFloat(document.getElementById('perimeter_se').value),
        area_se: parseFloat(document.getElementById('area_se').value),
        smoothness_se: parseFloat(document.getElementById('smoothness_se').value),
        compactness_se: parseFloat(document.getElementById('compactness_se').value),
        concavity_se: parseFloat(document.getElementById('concavity_se').value),
        concave_points_se: parseFloat(document.getElementById('concave_points_se').value),
        symmetry_se: parseFloat(document.getElementById('symmetry_se').value),
        fractal_dimension_se: parseFloat(document.getElementById('fractal_dimension_se').value),
        radius_worst: parseFloat(document.getElementById('radius_worst').value),
        texture_worst: parseFloat(document.getElementById('texture_worst').value),
        perimeter_worst: parseFloat(document.getElementById('perimeter_worst').value),
        area_worst: parseFloat(document.getElementById('area_worst').value),
        smoothness_worst: parseFloat(document.getElementById('smoothness_worst').value),
        compactness_worst: parseFloat(document.getElementById('compactness_worst').value),
        concavity_worst: parseFloat(document.getElementById('concavity_worst').value),
        concave_points_worst: parseFloat(document.getElementById('concave_points_worst').value),
        symmetry_worst: parseFloat(document.getElementById('symmetry_worst').value),
    };

    // Send POST request to the API
    fetch('http://localhost:5000/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(defaultFeatures),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
        alert(`Prediction Successful, ${data.prediction[0]}`);
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("An error occurred.");
    });

    return false; // Prevent default form submission
}

// Reset the form when the page loads
window.onload = function() {
    const form = document.querySelector('form');
    if (form) {
        form.reset();
    }
};