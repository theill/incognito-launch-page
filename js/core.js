var uuid;

function setUniqueIdentifier(id) {
	uuid = id;
	document.getElementById("user_uuid").value = id;
}

var sentences = ["i love", "i hate", "i think", "i believe", "i feel", "i wish"];

var casualBrowsing = {
	sentence: sentences[Math.floor(Math.random()*sentences.length)],
	
	randomChange: function() {
		this.sentence = sentences[Math.floor(Math.random() * sentences.length)];
		
		$("#available-sentences li").removeClass("selected");
		$("#available-sentences ul li." + this.sentence.replace(/ /g, '-')).addClass("selected");
		
		this.setup();
	},
	
	sentenceClassName: function() {
		return this.sentence.replace(/ /g, '-');
	},
	
	setup: function() {
		var cs = this;
		
		var sentenceRegEx = new RegExp(cs.sentence, "gi");

		$("#twitterSearch").liveTwitter('"' + cs.sentence + '"', { limit: 5, rate: 3000, lang: 'en', timeLinks: false }, function(container, newCount) {
			texts = $(container).find(".tweet p.text");
			$(texts).each(function(cnt, p) {
				$(p).html($(p).html().replace(sentenceRegEx, "<span class=\"" + cs.sentenceClassName() + "\">" + cs.sentence + "</span>"));
			});
		});
		
		window.setTimeout('casualBrowsing.randomChange()', 60 * 1000);
	}
};

$(function() {
	$("#available-sentences").html("<ul>" + $.map(sentences, function(ia, idx) {
		return "<li data-sentence=\"" + ia + "\" class='" + ia.replace(/ /g, '-') + "'><span>" + ia + "</span></li>"
		}).join("") + "</ul>");
	
	$("#available-sentences ul li").click(function() {
		$("#available-sentences li").removeClass("selected");
		
		$(this).addClass("selected");
		
		casualBrowsing.sentence = $(this).attr("data-sentence");
		casualBrowsing.setup();
	});
	
	casualBrowsing.randomChange();
	
	if (window.localStorage) {
		window.localStorage.clear();
	}
	
	if (window.sessionStorage) {
		window.sessionStorage.clear();
	}
	
	if (window.openDatabase) {
		var database = window.openDatabase("sqlite_evercookie", "", "evercookie", 1024 * 1024);
		database.transaction(function(tx) {
			tx.executeSql("DROP TABLE cache", [], function (tx, rs) { }, function (tx, err) { });
			tx.executeSql("DROP TABLE sqlite_sequence", [], function (tx, rs) { }, function (tx, err) { });
		});
	}
	
});