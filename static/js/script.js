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
 * BULLETPROOF VERSION: If a file exists, it turns GREEN. No complex checks.
 */
function updateScanStatus(file) {
    const checkIcon = document.getElementById('scanStatusCheck');
    const scannerText = document.getElementById('scannerText');
    const scannerIcon = document.getElementById('scannerIcon');

    // SIMPLEST LOGIC POSSIBLE: Do we have a file?
    if (file) {
        // 1. Show Green Checkmark
        checkIcon.classList.remove('hidden');
        
        // 2. Turn Text Green
        scannerText.classList.add('text-green-600');
        scannerText.classList.remove('text-gray-700');
        
        // 3. Update Icon & Text
        // We do a basic name check just for the icon, but the STATE is always green now.
        const fileName = file.name || '';
        const isVideo = file.type.startsWith('video/') || /\.(mp4|mov|avi|mkv|wmv|qt)$/i.test(fileName);

        if (isVideo) {
            scannerText.textContent = 'Video Ready!';
            scannerIcon.className = 'ph ph-video-camera text-4xl text-green-500'; 
        } else {
            scannerText.textContent = 'Image Ready!';
            scannerIcon.className = 'ph ph-image text-4xl text-green-500'; 
        }
        
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
        if (this.files && this.files.length > 0) {
            // Instant update
            updateScanStatus(this.files[0]); 
        } else {
            updateScanStatus(null); 
        }
    });
}

// FORCE LOADING SCREEN ON IPHONE
function attachFormSubmit() {
    const form = document.getElementById('scanForm');
    if (!form) return;

    form.addEventListener('submit', function(e) {
        // 1. PAUSE submission
        e.preventDefault();
        
        const hudOverlay = document.getElementById('hudOverlay');
        
        // 2. Force the overlay to appear
        hudOverlay.classList.remove('hidden');
        // This line forces the browser to paint the new pixels immediately
        void hudOverlay.offsetWidth; 

        // 3. Fade it in
        hudOverlay.classList.remove('opacity-0');
        hudOverlay.classList.add('opacity-100');

        // 4. WAIT 100ms, THEN submit. 
        // This gives the iPhone GPU time to render the overlay before the network freezes it.
        setTimeout(() => {
            form.submit();
        }, 150); 
    });
}

document.addEventListener('DOMContentLoaded', () => {
    showInput('file');
    attachTapEffect();
    attachFormSubmit(); 
});