(function() {
  "use strict";

  /**
   * Easy selector helper function
   */
  const select = (el, all = false) => {
    el = el.trim()
    if (all) {
      return [...document.querySelectorAll(el)]
    } else {
      return document.querySelector(el)
    }
  }

  /**
   * Easy event listener function
   */
  const on = (type, el, listener, all = false) => {
    if (all) {
      select(el, all).forEach(e => e.addEventListener(type, listener))
    } else {
      select(el, all).addEventListener(type, listener)
    }
  }

  /**
   * Easy on scroll event listener 
   */
  const onscroll = (el, listener) => {
    el.addEventListener('scroll', listener)
  }

  /**
   * Sidebar toggle
   */
  if (select('.toggle-sidebar-btn')) {
    on('click', '.toggle-sidebar-btn', function(e) {
      select('body').classList.toggle('toggle-sidebar')
    })
  }

  /**
   * Search bar toggle
   */
  if (select('.search-bar-toggle')) {
    on('click', '.search-bar-toggle', function(e) {
      select('.search-bar').classList.toggle('search-bar-show')
    })
  }

  /**
   * Navbar links active state on scroll
   */
  let navbarlinks = select('#navbar .scrollto', true)
  const navbarlinksActive = () => {
    let position = window.scrollY + 200
    navbarlinks.forEach(navbarlink => {
      if (!navbarlink.hash) return
      let section = select(navbarlink.hash)
      if (!section) return
      if (position >= section.offsetTop && position <= (section.offsetTop + section.offsetHeight)) {
        navbarlink.classList.add('active')
      } else {
        navbarlink.classList.remove('active')
      }
    })
  }
  window.addEventListener('load', navbarlinksActive)
  onscroll(document, navbarlinksActive)

  /**
   * Toggle .header-scrolled class to #header when page is scrolled
   */
  let selectHeader = select('#header')
  if (selectHeader) {
    const headerScrolled = () => {
      if (window.scrollY > 100) {
        selectHeader.classList.add('header-scrolled')
      } else {
        selectHeader.classList.remove('header-scrolled')
      }
    }
    window.addEventListener('load', headerScrolled)
    onscroll(document, headerScrolled)
  }

  /**
   * Back to top button
   */
  let backtotop = select('.back-to-top')
  if (backtotop) {
    const toggleBacktotop = () => {
      if (window.scrollY > 100) {
        backtotop.classList.add('active')
      } else {
        backtotop.classList.remove('active')
      }
    }
    window.addEventListener('load', toggleBacktotop)
    onscroll(document, toggleBacktotop)
  }

  /**
   * Initiate tooltips
   */
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

  /**
   * Initiate quill editors
   */
  if (select('.quill-editor-default')) {
    new Quill('.quill-editor-default', {
      theme: 'snow'
    });
  }

  if (select('.quill-editor-bubble')) {
    new Quill('.quill-editor-bubble', {
      theme: 'bubble'
    });
  }

  if (select('.quill-editor-full')) {
    new Quill(".quill-editor-full", {
      modules: {
        toolbar: [
          [{
            font: []
          }, {
            size: []
          }],
          ["bold", "italic", "underline", "strike"],
          [{
              color: []
            },
            {
              background: []
            }
          ],
          [{
              script: "super"
            },
            {
              script: "sub"
            }
          ],
          [{
              list: "ordered"
            },
            {
              list: "bullet"
            },
            {
              indent: "-1"
            },
            {
              indent: "+1"
            }
          ],
          ["direction", {
            align: []
          }],
          ["link", "image", "video"],
          ["clean"]
        ]
      },
      theme: "snow"
    });
  }

  /**
   * Initiate TinyMCE Editor
   */
  const useDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const isSmallScreen = window.matchMedia('(max-width: 1023.5px)').matches;

  tinymce.init({
    selector: 'textarea.tinymce-editor',
    plugins: 'preview importcss searchreplace autolink autosave save directionality code visualblocks visualchars fullscreen image link media template codesample table charmap pagebreak nonbreaking anchor insertdatetime advlist lists wordcount help charmap quickbars emoticons',
    editimage_cors_hosts: ['picsum.photos'],
    menubar: 'file edit view insert format tools table help',
    toolbar: 'undo redo | bold italic underline strikethrough | fontfamily fontsize blocks | alignleft aligncenter alignright alignjustify | outdent indent |  numlist bullist | forecolor backcolor removeformat | pagebreak | charmap emoticons | fullscreen  preview save print | insertfile image media template link anchor codesample | ltr rtl',
    toolbar_sticky: true,
    toolbar_sticky_offset: isSmallScreen ? 102 : 108,
    autosave_ask_before_unload: true,
    autosave_interval: '30s',
    autosave_prefix: '{path}{query}-{id}-',
    autosave_restore_when_empty: false,
    autosave_retention: '2m',
    image_advtab: true,
    link_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_list: [{
        title: 'My page 1',
        value: 'https://www.tiny.cloud'
      },
      {
        title: 'My page 2',
        value: 'http://www.moxiecode.com'
      }
    ],
    image_class_list: [{
        title: 'None',
        value: ''
      },
      {
        title: 'Some class',
        value: 'class-name'
      }
    ],
    importcss_append: true,
    file_picker_callback: (callback, value, meta) => {
      /* Provide file and text for the link dialog */
      if (meta.filetype === 'file') {
        callback('https://www.google.com/logos/google.jpg', {
          text: 'My text'
        });
      }

      /* Provide image and alt text for the image dialog */
      if (meta.filetype === 'image') {
        callback('https://www.google.com/logos/google.jpg', {
          alt: 'My alt text'
        });
      }

      /* Provide alternative source and posted for the media dialog */
      if (meta.filetype === 'media') {
        callback('movie.mp4', {
          source2: 'alt.ogg',
          poster: 'https://www.google.com/logos/google.jpg'
        });
      }
    },
    templates: [{
        title: 'New Table',
        description: 'creates a new table',
        content: '<div class="mceTmpl"><table width="98%%"  border="0" cellspacing="0" cellpadding="0"><tr><th scope="col"> </th><th scope="col"> </th></tr><tr><td> </td><td> </td></tr></table></div>'
      },
      {
        title: 'Starting my story',
        description: 'A cure for writers block',
        content: 'Once upon a time...'
      },
      {
        title: 'New list with dates',
        description: 'New List with dates',
        content: '<div class="mceTmpl"><span class="cdate">cdate</span><br><span class="mdate">mdate</span><h2>My List</h2><ul><li></li><li></li></ul></div>'
      }
    ],
    template_cdate_format: '[Date Created (CDATE): %m/%d/%Y : %H:%M:%S]',
    template_mdate_format: '[Date Modified (MDATE): %m/%d/%Y : %H:%M:%S]',
    height: 600,
    image_caption: true,
    quickbars_selection_toolbar: 'bold italic | quicklink h2 h3 blockquote quickimage quicktable',
    noneditable_class: 'mceNonEditable',
    toolbar_mode: 'sliding',
    contextmenu: 'link image table',
    skin: useDarkMode ? 'oxide-dark' : 'oxide',
    content_css: useDarkMode ? 'dark' : 'default',
    content_style: 'body { font-family:Helvetica,Arial,sans-serif; font-size:16px }'
  });

  /**
   * Initiate Bootstrap validation check
   */
  var needsValidation = document.querySelectorAll('.needs-validation')

  Array.prototype.slice.call(needsValidation)
    .forEach(function(form) {
      form.addEventListener('submit', function(event) {
        if (!form.checkValidity()) {
          event.preventDefault()
          event.stopPropagation()
        }

        form.classList.add('was-validated')
      }, false)
    })

  /**
   * Initiate Datatables
   */
  const datatables = select('.datatable', true)
  datatables.forEach(datatable => {
    new simpleDatatables.DataTable(datatable);
  })

  /**
   * Autoresize echart charts
   */
  const mainContainer = select('#main');
  if (mainContainer) {
    setTimeout(() => {
      new ResizeObserver(function() {
        select('.echart', true).forEach(getEchart => {
          echarts.getInstanceByDom(getEchart).resize();
        })
      }).observe(mainContainer);
    }, 200);
  }

  if (document.getElementById("record-book")) {
    if (!document.getElementById("isCover")) {
      const selectImageButton = document.getElementById("select-image-button");
      const imageInput = document.getElementById("image-input");

      selectImageButton.addEventListener("click", () => {
        imageInput.click();
      });

      imageInput.addEventListener("change", () => {
        document.getElementById("image-form").submit();
      });

    } else if (!document.getElementById("isSummary")) {

      const selectFileButton = document.getElementById("select-file-button");
      const fileInput = document.getElementById("file-input");

      selectFileButton.addEventListener("click", () => {
        fileInput.click();
      })

      fileInput.addEventListener("change", () => {
        document.getElementById("file-form").submit();
      });
    }
  }

  if (document.getElementById("book_query")) {
    const form = document.getElementById('mfqf');
    const inputsAndSelects = form.querySelectorAll('input[type="text"], select, textarea');

    inputsAndSelects.forEach(input => {
      const originalValue = input.value;

      const handleChange = () => {
        if (input.value !== originalValue) {
          input.classList.add('is-valid');
        } else {
          input.classList.remove('is-valid');
        }
      };

      if (input.tagName === 'INPUT' || input.tagName === "TEXTAREA") {
        input.addEventListener('input', handleChange);
      } else if (input.tagName === 'SELECT') {
        input.addEventListener('change', handleChange);
      }
    });
  }



  if (document.getElementById("login-form")) {
    const form = document.getElementById("login-form");
    const inputs = form.querySelectorAll('input[type="email"] input[type="password"]');

    function validateInput(event) {
        const input = event.target;
        if (input.value === '') {
            input.classList.add('is-invalid');
        } else {
            input.classList.remove('is-invalid');

        }

    }

    // Add event listener to each input field
    inputs.forEach(input => {
        input.addEventListener('blur', validateInput);

    });

  }




  if (document.getElementById('register-form')) {
    const passwordInput = document.getElementById('yourPassword');
    const confirmInput = document.getElementById('confirmPassword');
    const invalidFeedback = document.querySelector('.invalid-feedback');
    const registerForm = document.querySelector("#register");
    const submitButton = registerForm.querySelector("button[type='submit']")

    document.querySelectorAll("input").forEach(input => {
        input.addEventListener("input", () => {
            const input_value = input.value.replace(/\\s+/g);
            if (input_value === "" && input.required) {
                input.classList.add("is-invalid");
                submitButton.disabled = true
            }
            else {
                console.log(input)
                input.classList.remove("is-invalid");
                submitButton.disabled = false
            }
            if (input.id === "confirmPassword" || input.id === "yourPassword") {
                if (confirmInput.value !== passwordInput.value && confirmInput.value !== "") {
                    input.classList.add('is-invalid');
                    submitButton.disabled = true

                } else {
                    input.classList.remove('is-invalid');
                    submitButton.disabled = false
                }
            }
        })
    })
    registerForm.addEventListener("submit", event => {
        const roleSelect = document.querySelector("select");
        if (roleSelect.value === "0") {
            event.preventDefault()
            event.stopPropagation()
            roleSelect.classList.add("is-invalid");
        }
        else {
            roleSelect.classList.remove("is-invalid");
        }
    })
  }

  if (document.getElementById("query_results")) {
      const elements = [document.getElementById('first'), document.getElementById('last'), document.getElementById('next'), document.getElementById('previous')];
      document.querySelectorAll('.num').forEach(number => {
          elements.push(number)
      })
      for (const elt of elements) {
        if (elt) {
            console.log(elt)
            elt.addEventListener('click', (event) => {
                event.preventDefault();
                elt.href = window.location.href;
                if (elt.href.indexOf('&page=') !== -1) {
                    elt.href = elt.href.slice(0, elt.href.indexOf('&page='));
                    elt.href += '&page=' + elt.dataset.page;
                    console.log(elt.dataset.page)
                } else {
                    elt.href += '&page=' + elt.dataset.page;
                }
                window.location.href = elt.href;
            });
        }
    }
  }

})();