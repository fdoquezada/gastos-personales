var mMessenger = function () {

    var winTarget = null;
    var messageList = {
        Success : { status: 0, message: "Transacción exitosa" },
        Failure : {status: 1, message:"Transacción fallida"}
    }
    var registeredSites = {
        FracasoTransbank: { url: "FracasoTransbank.aspx", msg: messageList.Failure },
        ExitoTransbank: { url: "ExitoTransbank.aspx", msg: messageList.Success }
    };

    var _init = function ( TargetWindow ) {
        if (TargetWindow === undefined || TargetWindow === null)
            return;
        winTarget = TargetWindow.opener || (TargetWindow.parent != window.top ? TargetWindow.parent : null);
        SetMessage(TargetWindow.location.toString());
    };

    var SetMessage = function (sender) {
        if (sender === undefined || sender === null)
            return;

        if (winTarget === null || winTarget === undefined)
            return;

        var currSite = undefined;
        for (site in registeredSites) {
            currSite = registeredSites[site];
            if (currSite.url === undefined)
                continue;
            if (sender.includes(currSite.url)) {
                SendMessage(currSite.msg);
                break;
            }
        }
        return;
    };

    var SendMessage = function ( objMessage ) {
        if (winTarget === null || winTarget === undefined)
            return;

        if (winTarget.postMessage === undefined)
            return;
        if (objMessage === undefined || objMessage === null)
            return;

        winTarget.postMessage(objMessage, "*");

    };

    var _public = {
        _init: _init,
        SendMessage : SendMessage
    };

    return _public;
}();

mMessenger._init(this.window);