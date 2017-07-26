function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

Array.prototype.contains = function ( needle ) {
    for (i in this) {
        if (this[i] == needle) return true;
    }
    return false;
}

function getLangFromFileExtension(extension){
    var returnVal = -1;
    $("#snip-lang > option").each(function() {
        if((returnVal == -1) && (this.text == "Text"))
        {
            returnVal = this.value;
        }
        var validExtnesions = $(this).data("extension").split(',');
        if(validExtnesions.contains(extension))
       {
            returnVal = this.value;
        }
    });
    return returnVal;
}

$(document).ready(function() {
    $("#search-help-tooltip").popover({
        trigger: 'hover',
        container: '.fa.fa-info'
    });

    var query = getParameterByName('query');
    if (query) {
        $("#snippet-search").attr('value', query);
    }

    $("#snippet-form").submit(function () {
        $("#submit-snippet-button").attr("disabled", true);
        return true;
	});
	
	$("#file-upload-btn").on("change",function(){
        var file  = this.files[0];
        var reader = new FileReader();
        reader.readAsText(file, "UTF-8");
        reader.onload = function (evt) {
            $("#snip-code").val(evt.target.result);
            $("#snip-title").val(file.name);
            $("#snip-description").val(file.name);
            var extension = file.name.split('.').pop();
            $("#snip-lang").val(getLangFromFileExtension(extension));
        }
    });
});


(function(){
	if (typeof self === 'undefined' || !self.Prism || !self.document) {
		return;
	}

	Prism.plugins.toolbar.registerButton('copy-to-clipboard', function (env) {
		var linkCopy = document.createElement('a');
		linkCopy.innerHTML = '<i class="fa fa-copy"></i>';

		if (!Clipboard) {
			callbacks.push(registerClipboard);
		} else {
			registerClipboard();
		}

		return linkCopy;

		function registerClipboard() {
			var clip = new Clipboard(linkCopy, {
				'text': function () {
					return env.code;
				}
			});

			clip.on('success', function() {
				linkCopy.textContent = 'Copied!';

				resetText();
			});
			clip.on('error', function () {
				linkCopy.textContent = 'Press Ctrl+C to copy';

				resetText();
			});
		}

		function resetText() {
			setTimeout(function () {
				linkCopy.innerHTML = '<i class="fa fa-copy"></i>';
			}, 1000);
		}
	});
})();


