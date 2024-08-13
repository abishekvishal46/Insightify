      function showTextBox() {
            document.getElementById('job-description-container').style.display = 'block';
            document.getElementById('file-uploader').style.display = 'none';
            document.getElementById('get-started-button').style.display = 'none';
        }


        function showUploader() {
            document.getElementById('job-description-container').style.display = 'none';
            document.getElementById('file-uploader').style.display = 'block';
        }

        function previewFile() {
            const file = document.getElementById('file-upload').files[0];
            const preview = document.getElementById('file-preview');
            const icon = document.querySelector('.upload-icon');
            const binButton = document.getElementById('bin-button');
            const reader = new FileReader();

            reader.onloadend = function () {
                icon.style.display = 'none';
                binButton.style.display = 'block';

                if (file.type === 'application/pdf') {
                    preview.innerHTML = `<iframe src="${reader.result}" frameborder="0"></iframe>`;
                    preview.style.display = 'block';
                }
            }

            if (file) {
                reader.readAsDataURL(file);
            } else {
                clearFile();
            }
        }

        function extractTextAndSend() {
            const file = document.getElementById('file-upload').files[0];
            const jobDescription = document.getElementById('job-description').value;

            if (!file) {
                alert("Please upload a file first.");
                return;
            }
            if (!jobDescription) {
                alert("Please enter the job description.");
                return;
            }

            extractTextFromPDF(file, jobDescription);
        }

       function extractTextFromPDF(file, jobDescription) {
    const reader = new FileReader();
    reader.onload = function() {
        const typedarray = new Uint8Array(this.result);

        pdfjsLib.getDocument(typedarray).promise.then(function(pdf) {
            let textContent = '';
            const numPages = pdf.numPages;
            let countPromises = [];

            for (let i = 1; i <= numPages; i++) {
                let page = pdf.getPage(i);

                let txt = "";
                countPromises.push(page.then(function(page) {
                    return page.getTextContent().then(function(text) {
                        for (let item of text.items) {
                            txt += item.str + " ";
                        }
                        textContent += txt + '\n';
                    });
                }));
            }

            Promise.all(countPromises).then(function() {
                console.log('Extracted text:', textContent); // Debug log
                sendTextToBackend(jobDescription, textContent);
            });
        });
    };
    reader.readAsArrayBuffer(file);
}

        function sendTextToBackend(jobDescription, pdfText) {
    fetch('/resume_extractor', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ job_description: jobDescription, pdf_text: pdfText })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok: ' + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log('Success:', data);

        if (data.success) {
            window.location.href = `/points?job_description=${encodeURIComponent(data.job_description)}&pdf_text=${encodeURIComponent(data.pdf_text)}`;
        } else {
            window.location.href = '/error';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        window.location.href = '/error';
    });
}


        function clearFile(event) {
            if (event) event.stopPropagation();
            const preview = document.getElementById('file-preview');
            const icon = document.querySelector('.upload-icon');
            const binButton = document.getElementById('bin-button');
            document.getElementById('file-upload').value = '';
            preview.innerHTML = '';
            preview.style.display = 'none';
            icon.style.display = 'block';
            binButton.style.display = 'none';
        }

        var TxtType = function(el, toRotate, period) {
            this.toRotate = toRotate;
            this.el = el;
            this.loopNum = 0;
            this.period = parseInt(period, 10) || 2000;
            this.txt = '';
            this.tick();
            this.isDeleting = false;
        };

        TxtType.prototype.tick = function() {
            var i = this.loopNum % this.toRotate.length;
            var fullTxt = this.toRotate[i];

            if (this.isDeleting) {
                this.txt = fullTxt.substring(0, this.txt.length - 1);
            } else {
                this.txt = fullTxt.substring(0, this.txt.length + 1);
            }

            this.el.innerHTML = '<span class="wrap">' + this.txt + '</span>';

            var that = this;
            var delta = 200 - Math.random() * 100;

            if (this.isDeleting) { delta /= 2; }

            if (!this.isDeleting && this.txt === fullTxt) {
                delta = this.period;
                this.isDeleting = true;
            } else if (this.isDeleting && this.txt === '') {
                this.isDeleting = false;
                this.loopNum++;
                delta = 500;
            }

            setTimeout(function() {
                that.tick();
            }, delta);
        };

        window.onload = function() {
            var elements = document.getElementsByClassName('typewrite');
            for (var i = 0; i < elements.length; i++) {
                var toRotate = elements[i].getAttribute('data-type');
                var period = elements[i].getAttribute('data-period');
                if (toRotate) {
                    new TxtType(elements[i], JSON.parse(toRotate), period);
                }
            }

            var css = document.createElement("style");
            css.type = "text/css";
            css.innerHTML = ".typewrite > .wrap { border-right: 0.08em solid #333}";
            document.body.appendChild(css);
        };