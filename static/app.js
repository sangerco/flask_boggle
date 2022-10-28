class BoggleGame {
    constructor(boardId, secs = 60){
        this.secs = secs;
        this.showTimer();
        this.score = 0;
        this.words = new Set();
        this.board = $("#" + boardId);

        this.timer = setInterval(this.tick.bind(this), 1000);
        $(".add-word", this.board).on("submit", this.handleSubmit.bind(this));
    }

    showWord(word) {
        $(".words", this.board).append($("<li>", { text: word }));
    }

    showScore() {
        $(".score").text(this.score);
        console.log(this.score);
    }

    showMessage(msg, cls) {
        $(".msg")
            .text(msg)
            .removeClass()
            .addClass(`msg ${cls}`);
        console.log(msg, cls)
    }

    async handleSubmit(e) {
        e.preventDefault();
        const $word = $('.word', this.board);

        let word = $word.val();
        if (!word) return;

        if (this.words.has(word)) {
            this.showMessage(`${word} has already been found!`, "err");
            return;
        }

        const res = await axios.get("/check_word", { params: { word: word } });
        console.log(res);
        if (res.data.result === "not-word") {
            this.showMessage(`${word} is not a valid word!`, "err");
        } else if (res.data.result === "not-on-board") {
            this.showMessage(`${word} is not on the board!`, "err");
        } else {
            this.showWord(word);
            this.score += word.length;
            this.showScore();
            this.words.add(word);
            this.showMessage(`Added ${word} to word list.`, "ok")
        }
        $word.val('').focus();
    }

    showTimer() {
        $(".timer").text(this.secs);
        console.log(this.secs)
    }

    async tick() {
        this.secs -= 1;
        this.showTimer();

        if (this.secs === 0) {
            clearInterval(this.timer);
            await this.scoreGame()
        }
    }

    async scoreGame() {
        $(".add-word", this.board).hide();
        const res = await axios.post('/post_score', { score: this.score });
        console.log(this.score);
        if (res.data.newHighScore) {
            this.showMessage(`New High Score! ${this.score}`, "ok")
        } else {
            this.showMessage(`Your score: ${this.score}`, "ok")
        }
    }
}

let game = new BoggleGame('boggle', 60)
