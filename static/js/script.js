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
        
        fileInput.required = true;
        videoInput.required = false;
        videoInput.value = ''; 
    } else if (type === 'video') {
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
 * Updates the visual status (Checkmark vs Upload Icon).
 */
function updateScanStatus(file) {
    const checkIcon = document.getElementById('scanStatusCheck');
    const scannerText = document.getElementById('scannerText');
    const scannerIcon = document.getElementById('scannerIcon');

    if (file) {
        // 1. Show the Stable Checkmark
        checkIcon.classList.remove('hidden');
        
        // 2. Detect Type and Change Text/Main Icon
        if (file.type.startsWith('video/')) {
            scannerText.textContent = 'Video Received!';
            scannerIcon.className = 'ph ph-video-camera text-4xl text-green-500'; 
        } else {
            scannerText.textContent = 'Photo Received!';
            scannerIcon.className = 'ph ph-image text-4xl text-green-500'; 
        }
        
        // 3. Make text green
        scannerText.classList.add('text-green-600');
        scannerText.classList.remove('text-gray-700');
        
    } else {
        // RESET TO DEFAULT
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
    
    // Visual flash when clicking
    fileInput.addEventListener('click', function() {
        filePanel.classList.add('border-blue-500', 'bg-blue-50');
        setTimeout(() => {
            filePanel.classList.remove('border-blue-500', 'bg-blue-50');
        }, 300); 
    });

    // Handle file selection
    fileInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            updateScanStatus(this.files[0]); 
        } else {
            updateScanStatus(null); 
        }
    });
}

// Loading Screen Animation
document.getElementById('scanForm').addEventListener('submit', function(e) {
    const hudOverlay = document.getElementById('hudOverlay');
    
    hudOverlay.classList.remove('hidden');

    setTimeout(() => {
        hudOverlay.classList.remove('opacity-0');
        hudOverlay.classList.add('opacity-100');
    }, 10); 
});


document.addEventListener('DOMContentLoaded', () => {
    showInput('file');
    attachTapEffect();
});