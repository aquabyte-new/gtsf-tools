// Validation is done via K-factor and equivalent relationships.

function kfactor(weight_g, dim_mm) {
    const dim_cm = dim_mm / 10;
    return weight_g * 100 / dim_cm ** 3;
}


export function isWeightValid(weight_g) {
    // Required
    if (weight_g === null || weight_g === "") return false;
    
    // Range Validations
    if (weight_g < 10) return false;
    if (weight_g > 15000) return false;

    // Return true if all validations pass
    return true;
}


export function isLengthValid(weight_g, length_mm) {
    // Required
    if (length_mm === null || length_mm === "") return false;

    // Range Validations
    if (length_mm < 50) return false;
    if (length_mm > 1500) return false;

    // KF Validations
    const kf = kfactor(weight_g, length_mm);
    if (kf < 0.3) return false;
    if (kf > 4.0) return false;

    // Return true if all validations pass
    return true;
}


export function isWidthValid(weight_g, width_mm) {
    // Optional
    if (width_mm === null || width_mm === "") return true;
    console.log("width_mm", width_mm);
    console.log("width_mm", typeof width_mm);

    // Range Validations
    if (width_mm < 10) return false;
    if (width_mm > 400) return false;

    // KF Validations
    const kf = kfactor(weight_g, width_mm);
    if (kf < 10) return false;
    if (kf > 250) return false;

    // Return true if all validations pass
    return true;
}


export function isBreadthValid(weight_g, breadth_mm) {
    // Optional
    if (breadth_mm === null || breadth_mm === "") return true;

    // Range Validations
    if (breadth_mm < 5) return false;
    if (breadth_mm > 250) return false;

    // KF Validations
    const kf = kfactor(weight_g, breadth_mm);
    if (kf < 200) return false;
    if (kf > 2500) return false;

    // Return true if all validations pass
    return true;
}