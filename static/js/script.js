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
 * FIXED: Now turns green for ANY file detection, ignoring iOS MIME type bugs.
 */
function updateScanStatus(file) {
    const checkIcon = document.getElementById('scanStatusCheck');
    const scannerText = document.getElementById('scannerText');
    const scannerIcon = document.getElementById('scannerIcon');

    // 1. Check if a file actually exists
    if (file) {
        // --- VISUAL SUCCESS STATE (GREEN) ---
        // We do this immediately so the user knows it worked
        checkIcon.classList.remove('hidden');
        scannerText.classList.add('text-green-600');
        scannerText.classList.remove('text-gray-700');

        // 2. DETECT TYPE (Robust iOS Fallback)
        // iOS often sends empty type for .mov files. We check name extension as backup.
        const fileType = file.type || ''; 
        const fileName = file.name || '';
        
        const isVideo = fileType.startsWith('video/') || 
                        fileType === 'video/quicktime' || 
                        /\.(mp4|mov|avi|mkv|wmv|qt)$/i.test(fileName);

        if (isVideo) {
            scannerText.textContent = 'Video Received!';
            scannerIcon.className = 'ph ph-video-camera text-4xl text-green-500'; 
        } else {
            // Default to image if it's not clearly a video
            scannerText.textContent = 'Photo Received!';
            scannerIcon.className = 'ph ph-image text-4xl text-green-500'; 
        }
        
    } else {
        // --- RESET TO DEFAULT STATE (BLUE) ---
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
    
    // Visual flash when clicking (Feedback)
    fileInput.addEventListener('click', function() {
        filePanel.classList.add('border-blue-500', 'bg-blue-50');
        setTimeout(() => {
            filePanel.classList.remove('border-blue-500', 'bg-blue-50');
        }, 300); 
    });

    // Handle file selection
    fileInput.addEventListener('change', function() {
        if (this.files && this.files.length > 0) {
            // Force a small delay to ensure iOS UI updates
            setTimeout(() => {
                updateScanStatus(this.files[0]);
            }, 50);
        } else {
            updateScanStatus(null); 
        }
    });
}

// Loading Screen Animation (iOS PWA Safe Version)
// We define this OUTSIDE of other functions to ensure it attaches on load
function attachFormSubmit() {
    const form = document.getElementById('scanForm');
    if (!form) return;

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
        // This is the "magic" fix for iOS PWA freezing
        setTimeout(() => {
            form.submit();
        }, 100); 
    });
}

// Initialize on Load
document.addEventListener('DOMContentLoaded', () => {
    showInput('file');
    attachTapEffect();
    attachFormSubmit(); // Attach the form listener
});