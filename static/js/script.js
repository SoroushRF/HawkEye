// --- 1. CORE FUNCTIONALITY ---

/**
 * Switches between file upload/camera input and video URL input.
 * Manages panel visibility and 'required' status for form submission validation.
 * @param {string} type - 'file' or 'video'
 */
function showInput(type) {
    const filePanel = document.getElementById('fileInputPanel');
    const videoPanel = document.getElementById('videoInputPanel');
    const fileTab = document.getElementById('tab-file');
    const videoTab = document.getElementById('tab-video');
    const fileInput = document.getElementById('file-upload');
    const videoInput = document.getElementById('video-url');

    if (type === 'file') {
        // Activate File/Camera Panel
        filePanel.classList.remove('hidden');
        videoPanel.classList.add('hidden');
        fileTab.classList.add('active');
        videoTab.classList.remove('active');
        
        fileInput.required = true;
        videoInput.required = false;
        videoInput.value = ''; 
    } else if (type === 'video') {
        // Activate Video URL Panel
        filePanel.classList.add('hidden');
        videoPanel.classList.remove('hidden');
        fileTab.classList.remove('active');
        videoTab.classList.add('active');

        fileInput.required = false;
        fileInput.value = ''; 
        videoInput.required = true;
    }
}

/**
 * Attaches the visual feedback effect to the file input click.
 */
function attachTapEffect() {
    document.getElementById('file-upload').addEventListener('click', function() {
        const icon = document.getElementById('scannerIcon');
        const text = document.getElementById('scannerText');
        const hint = document.getElementById('scannerHint');
        const scannerBorder = document.getElementById('scannerBorder');

        // --- Visual Confirmation (Target Lock) ---
        icon.classList.remove('ph-camera', 'text-emerald-400');
        icon.classList.add('ph-check-circle', 'text-red-500', 'animate-pulse');
        scannerBorder.classList.add('border-red-500');
        scannerBorder.classList.remove('border-blue-500/50');

        text.textContent = 'CAMERA ACTIVATED';
        text.classList.add('text-red-400');
        text.classList.remove('text-slate-300');

        hint.textContent = 'SCAN INITIATED...';
        hint.classList.add('text-red-400');
        hint.classList.remove('text-blue-500');

        // --- Revert After a Short Delay (0.8s) ---
        setTimeout(() => {
            icon.classList.remove('ph-check-circle', 'text-red-500', 'animate-pulse');
            icon.classList.add('ph-camera', 'text-emerald-400');
            scannerBorder.classList.remove('border-red-500');
            scannerBorder.classList.add('border-blue-500/50');
            
            text.textContent = 'INITIATE LIVE SCAN';
            text.classList.remove('text-red-400');
            text.classList.add('text-slate-300');

            hint.textContent = '(Tap to activate camera/video capture)';
            hint.classList.remove('text-red-400');
            hint.classList.add('text-blue-500');
        }, 800); 
    });
}

/**
 * Updates the AI Confidence Threshold display value in real-time.
 */
function attachSliderListener() {
    const slider = document.getElementById('confidence');
    const valueDisplay = document.getElementById('confidenceValue');
    
    // Set initial value
    valueDisplay.textContent = slider.value + '%';

    slider.addEventListener('input', function() {
        valueDisplay.textContent = this.value + '%';
    });
}

// --- 2. INITIALIZATION ---

document.addEventListener('DOMContentLoaded', () => {
    // Initialize the tab visibility
    showInput('file');
    // Attach the visual effect listener
    attachTapEffect();
    // Attach the slider update listener
    attachSliderListener();
});