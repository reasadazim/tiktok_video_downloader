$( document ).ready(function() {

    // On reload open the download tab
    setTimeout(() => {

        var hash = window.location.hash;
        if (hash != ''){
            hash = hash. substring(1);
            var nav = '#nav-';
            var tab = '-tab';
            hash = nav.concat(hash);
            hash = hash.concat(tab);
            var hash1 = hash.substring(0,hash.length - 4);

            $(".tab-pane").removeClass('show');
            $(".tab-pane").removeClass('active');

            $(".nav-link").removeClass('active');
            $(".nav-link").attr('aria-selected', false);

            $(hash).addClass('active');
            $(hash).attr('aria-selected', true);
            $(hash).removeAttr('tabindex');

            $(hash1).addClass('active');
            $(hash1).addClass('show');

            $(hash).trigger( "click" );
        }

    }, "500");

    // On click open the download tab
    $(".click-trigger").click(function(){

        setTimeout(() => {

            var hash = window.location.hash;
            hash = hash. substring(1);
            var nav = '#nav-';
            var tab = '-tab';
            hash = nav.concat(hash);
            hash = hash.concat(tab);
            var hash1 = hash.substring(0,hash.length - 4);

            $(".tab-pane").removeClass('show');
            $(".tab-pane").removeClass('active');

            $(".nav-link").removeClass('active');
            $(".nav-link").attr('aria-selected', false);

            $(hash).addClass('active');
            $(hash).attr('aria-selected', true);
            $(hash).removeAttr('tabindex');

            $(hash1).addClass('active');
            $(hash1).addClass('show');

            $(hash).trigger( "click" );

        }, "200");

    });

    // On click show loader
    $("form").submit(function(){
        $('.loader').show();
    });

    // Validate input URL
    setInterval(function (){

        var url = $('#url').val();

        if (url != ''){
            let domain = (new URL(url));
            domain = domain.hostname;
            console.log(domain)
            if ((domain == 'www.tiktok.com')||(domain == 'vt.tiktok.com')){
                const regex = new RegExp("/video/",);
                if (regex.test(url)){
                    url = url.replace(/\?.*$/g,"");
                    url = url+'?__a=1&__d=dis';
                    $('#scrap_url').val(url);
                }else{
                    if (domain != 'vt.tiktok.com'){
                        $('#url').val('');
                        $('#scrap_url').val('');
                        alert("The URL you pasted is not an TikTok video URL!");
                    }
                }
            }else{
                $('#url').val('');
                $('#scrap_url').val('');
                alert("The URL you pasted is not an TikTok URL!");
            }
        }else{
            $('#scrap_url').val('');
        }

    },1000)

});


