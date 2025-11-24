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
 * PATCHED: Now supports iOS .mov and QuickTime video detection.
 */
function updateScanStatus(file) {
    const checkIcon = document.getElementById('scanStatusCheck');
    const scannerText = document.getElementById('scannerText');
    const scannerIcon = document.getElementById('scannerIcon');

    if (file) {
        // 1. Show the Stable Checkmark
        checkIcon.classList.remove('hidden');
        
        // 2. DETECT TYPE (Robust iOS Check)
        // Check MIME type OR file extension
        const isVideo = file.type.startsWith('video/') || 
                        file.type === 'video/quicktime' || 
                        /\.(mp4|mov|avi|mkv|wmv)$/i.test(file.name);

        if (isVideo) {
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
// Loading Screen Animation (iOS PWA Safe Version)
const form = document.getElementById('scanForm');

form.addEventListener('submit', function(e) {
    // 1. STOP the immediate send. We need to show the UI first.
    e.preventDefault();
    
    const hudOverlay = document.getElementById('hudOverlay');
    
    // 2. Show the loading screen
    hudOverlay.classList.remove('hidden');
    // Force a browser reflow (paint frame)
    void hudOverlay.offsetWidth; 

    // 3. Fade it in
    requestAnimationFrame(() => {
        hudOverlay.classList.remove('opacity-0');
        hudOverlay.classList.add('opacity-100');
    });

    // 4. WAIT 100ms for the iPhone to render the new UI, THEN submit.
    setTimeout(() => {
        form.submit();
    }, 100); 
});


document.addEventListener('DOMContentLoaded', () => {
    showInput('file');
    attachTapEffect();
});