// http://twitter.com/home?status={{title}}%20{{url}}%20by%20
// https://www.facebook.com/sharer/sharer.php?u={{url}}
// https://plus.google.com/share?url={{url}}
// http://b.hatena.ne.jp/add?mode=confirm&url={{url}}
// http://getpocket.com/edit?url={{url}}

$(document).ready(function(){
    /* for navbar */
    window.addEventListener("hashchange", function() { scrollBy(0, -70) });

    /* social buttons */
    var url = location.href;
    var title = $('title').text();
    $('.share-twitter').find('a').attr('href', 'http://twitter.com/home?status='+title+'%20'+url+'%20via%20@hiroharu_kato');
    $('.share-facebook').find('a').attr('href', 'https://www.facebook.com/sharer/sharer.php?u='+url);
    $('.share-google').find('a').attr('href', 'https://plus.google.com/share?url='+url);
    $('.share-hatena').find('a').attr('href', 'http://b.hatena.ne.jp/add?mode=confirm&url='+url);
    $('.share-pocket').find('a').attr('href', 'http://getpocket.com/edit?url='+url);

    /* outer link */
    $("a").each(function(i, val) {
        val = $(val);
        if (val.attr('href') && val.attr('href').substr(0, 4) == 'http') {
            val.attr('target', '_blank');
        }
    })
});

