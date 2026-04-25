


let lastBacktestResult = null;

function formatDate(dateString) {
    const date = new Date(dateString);

    return date.toLocaleString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit"
    });
}


$(document).ready(function () {

    $("#backtest-form").on("submit", function (e) {
        e.preventDefault();

        const button = $("#run-btn");
        const errorBox = $("#error-box");

        errorBox.addClass("hidden").text("");
        button.prop("disabled", true).text("Running...");

        const payload = {
            coin: $("select[name='coin']").val(),
            currency: $("select[name='currency']").val(),
            period: $("select[name='period']").val(),
            interval: $("select[name='interval']").val(),
            fast_ema: parseInt($("input[name='fast_ema']").val()),
            slow_ema: parseInt($("input[name='slow_ema']").val())
        };

        $.ajax({
            url: "/backtest/run",
            method: "POST",
            contentType: "application/json",
            data: JSON.stringify(payload),
            success: function (response) {
                console.log(response.payload);
                const data = response.payload;
                const metrics = data.metrics;

                $("#results-card").removeClass("hidden");

                $("#total-return").text(`${metrics.total_return}%`);
                $("#win-rate").text(`${metrics.win_rate}%`);
                $("#max-drawdown").text(`${metrics.max_drawdown}%`);
                $("#number-of-trades").text(metrics.number_of_trades);

                const tbody = $("#trades-body");
                tbody.empty();

                lastBacktestResult = data;
                data.trades.forEach(function (trade) {
                    console.log(trade);
                    tbody.append(`
                        <tr class="border-b border-slate-200"> 
                            <td class="py-2 text-start">${formatDate(trade.entry_time)}</td>
                            <td class="py-2 text-start">${formatDate(trade.exit_time)}</td>
                            <td class="py-2 text-start">${trade.duration}</td>
                            <td class="py-2 text-start">${trade.entry_price}</td>
                            <td class="py-2 text-start">${trade.exit_price}</td>
                            <td class="py-2 text-start ${trade.profit >= 0 ? 'text-green-600' : 'text-red-600'}">
                                ${trade.profit}
                            </td>
                        </tr>
                    `);
                });
            },
            error: function (xhr) {
                const message = xhr.responseJSON?.message || "Failed to run backtest";
                errorBox.removeClass("hidden").text(message);
            },
            complete: function () {
                button.prop("disabled", false).text("Run Backtest");
            }
        });
    });

    $("#download-btn").click(function () {
        if (!lastBacktestResult) return;

        const symbol = lastBacktestResult.symbol;
        const period = lastBacktestResult.period;
        const interval = lastBacktestResult.interval;
        const strategy = (lastBacktestResult.strategy)
            .toLowerCase()
            .replaceAll(" ", "_")
            .replaceAll("/", "_");

        const fileName = `backtest_${symbol}_${period}_${interval}_${strategy}.json`;


        const blob = new Blob(
            [JSON.stringify(lastBacktestResult, null, 2)],
            { type: "application/json" }
        );

        const url = URL.createObjectURL(blob);

        const a = document.createElement("a");
        a.href = url;
        a.download = fileName;
        a.click();

        URL.revokeObjectURL(url);
    });

});