// --- 1. CORE FUNCTIONALITY ---

function showInput(type) {
    const filePanel = document.getElementById('fileInputPanel');
    const videoPanel = document.getElementById('videoInputPanel');
    const fileTab = document.getElementById('tab-file');
    const videoTab = document.getElementById('tab-video');
    const fileInput = document.getElementById('file-upload');
    const videoInput = document.getElementById('video-url');

    if (type === 'file') {
        filePanel.classList.remove('hidden');
        videoPanel.classList.add('hidden');
        fileTab.classList.add('active');
        videoTab.classList.remove('active');
        
        // Reset and require
        fileInput.required = true;
        videoInput.required = false;
        videoInput.value = ''; 
    } else if (type === 'video') {
        filePanel.classList.add('hidden');
        videoPanel.classList.remove('hidden');
        fileTab.classList.remove('active');
        videoTab.classList.add('active');

        // Reset and require
        fileInput.required = false;
        fileInput.value = ''; 
        videoInput.required = true;
    }
}

/**
 * VISUAL FEEDBACK: Green Box Logic
 * If a file exists in the array, we turn green. Simple as that.
 */
function updateScanStatus(hasFile) {
    const checkIcon = document.getElementById('scanStatusCheck');
    const scannerText = document.getElementById('scannerText');
    const scannerIcon = document.getElementById('scannerIcon');

    if (hasFile) {
        // --- GREEN SUCCESS STATE ---
        checkIcon.classList.remove('hidden');
        
        scannerText.textContent = 'Media Ready!';
        scannerText.classList.add('text-green-600');
        scannerText.classList.remove('text-gray-700');
        
        // Universal Success Icon
        scannerIcon.className = 'ph ph-check-circle text-4xl text-green-500'; 
        
    } else {
        // --- DEFAULT BLUE STATE ---
        checkIcon.classList.add('hidden');
        scannerText.textContent = 'Upload Photo or Video';
        scannerText.classList.remove('text-green-600');
        scannerText.classList.add('text-gray-700');
        
        scannerIcon.className = 'ph ph-upload-simple text-4xl text-blue-500'; 
    }
}

function attachTapEffect() {
    const fileInput = document.getElementById('file-upload');
    const filePanel = document.getElementById('fileInputPanel');
    
    // 1. Click Animation
    fileInput.addEventListener('click', function() {
        filePanel.classList.add('border-blue-500', 'bg-blue-50');
        setTimeout(() => {
            filePanel.classList.remove('border-blue-500', 'bg-blue-50');
        }, 300); 
    });

    // 2. Change Listener (The Green Box Trigger)
    fileInput.addEventListener('change', function() {
        // iOS sometimes takes a ms to update the files array, so we check existence
        const hasFiles = this.files && this.files.length > 0;
        updateScanStatus(hasFiles);
    });
}

function attachFormSubmit() {
    const form = document.getElementById('scanForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        // 1. STOP the form immediately
        e.preventDefault();
        
        const hudOverlay = document.getElementById('hudOverlay');
        
        // 2. Force the Overlay to Appear
        hudOverlay.classList.remove('hidden');
        
        // 3. MAGIC TRICK: Force browser to paint pixels
        // Accessing offsetWidth forces a reflow, ensuring the UI updates visually
        void hudOverlay.offsetWidth; 

        // 4. Fade In
        hudOverlay.classList.remove('opacity-0');
        hudOverlay.classList.add('opacity-100');

        // 5. WAIT for the paint to finish (200ms), THEN Submit
        // This ensures the "Analyzing" screen is visible before the network locks the UI.
        setTimeout(() => {
            form.submit();
        }, 200); 
    });
}

// Fix for Safari "Back Button" leaving the overlay on screen
window.addEventListener("pageshow", function(event) {
    const hudOverlay = document.getElementById('hudOverlay');
    if (event.persisted || (window.performance && window.performance.navigation.type === 2)) {
        if(hudOverlay) {
            hudOverlay.classList.add('hidden');
            hudOverlay.classList.add('opacity-0');
        }
    }
});

// INITIALIZE
document.addEventListener('DOMContentLoaded', () => {
    // Default to file view
    showInput('file');
    // Attach event listeners
    attachTapEffect();
    attachFormSubmit(); 
});