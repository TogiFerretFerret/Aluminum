"use strict";
/**
 * @type {HTMLFormElement}
 */
const form = document.getElementById("uv-form");
/**
 * @type {HTMLParagraphElement}
 */
const error = document.getElementById("uv-error");
/**
 * @type {HTMLPreElement}
 */
const errorCode = document.getElementById("uv-error-code");
const connection = new BareMux.BareMuxConnection("/baremux/worker.js")
function reverseEncoding(encodedStr) {
    return decodeURIComponent(encodedStr)
        .split('')
        .map((char, ind) =>
            ind % 2 ? String.fromCharCode(char.charCodeAt() ^ 2) : char
        )
        .join('');
}
async function main(url, redirector){


	try {
		await registerSW();
	} catch (err) {
		error.textContent = "Failed to register service worker.";
		errorCode.textContent = err.toString();
		throw err;
	}
	let frame = document.getElementById("uv-frame");
	frame.style.display = "block";
	let wispUrl = (location.protocol === "https:" ? "wss" : "ws") + "://" + location.host + "/wisp/";
	if (await connection.getTransport() !== "/epoxy/index.mjs") {
		await connection.setTransport("/epoxy/index.mjs", [{ wisp: wispUrl }]);
	}
	frame.src = __uv$config.prefix + __uv$config.encodeUrl(url);
	console.log(url)
	console.log(frame.src);
	var dostop=false;
	setInterval(() => {
		var test=frame.contentWindow.location.href;
		test=reverseEncoding(test.split("/uv/service/")[1]);
		if (test.startsWith("https://sts.sky.blackbaud.com/") && !dostop) {
			location.href = redirector+"/seturl?url="+btoa(test);
			dostop=true;
		}
	}, 200);
}
(()=>{
	let params = location.search
	let redirector=params.split("redirector=")[1].split("&")[0];
	console.log(params);
	let url=params.split("url=")[1];
	main((url), redirector);
})();