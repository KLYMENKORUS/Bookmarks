(function (){
    if (window.myBookmarklet !== undefined){
        myBookmarklet();
    }
    else {
        document.body.appendChild(
            document.createElement('script')
        ).src='https://80bf-185-181-166-81.eu.ngrok.io/static/js/bookmarklet.js?r='+
            Math.floor(Math.random()*99999999999999999999)
    }
})();