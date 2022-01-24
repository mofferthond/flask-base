from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user
)
from sqlalchemy import select
from app import db
from app.decorators import admin_required
from app.models import EditableHTML
from app.models.user import User, Role

from app.wakkerdam.forms import CreateGameForm, InvitePlayersForm, NewMessageForm
from app.wakkerdam.models import *

wakkerdam = Blueprint('wakkerdam', __name__)

# CU = current user
@wakkerdam.route('/games')
@login_required
def games():
    # Select all games for CU
    # Select amount of invites for CU
   
    games = [player.getGame() for player in current_user.getPlayers()]
    # render games.html
    # @require games, current_user{>getInviteAmount()}
    return render_template('wakkerdam/games.html', title="Jouw spellen", games=games, current_user=current_user)

@wakkerdam.route('/game/<int:gameId>', methods=['GET', 'POST'])
@login_required
def game(gameId):
    # Select game with id gameId
    game = Game.query.filter_by(_id=gameId).first()
    print(current_user.getPlayer(game).getAvailableActions())
    
    # @aborts
    #   - game does not exist
    #   - CU not in game
    if game == None:
        flash("Je zit niet in dit spel", "error")
        return redirect(url_for("wakkerdam.games"))
    if current_user not in [player.getUser() for player in game.getPlayers()]:
        flash("Je zit niet in dit spel", "error")
        return redirect(url_for("wakkerdam.games"))


    # Form : InvitePlayersForm (invite new user to game)
    #   - only for game host
    #   @aborts
    #       - CU is not host
    #       - invite for CU
    #       - user does not exist
    #       - user is already in game
    #       - user is already invited
    #   @actions
    #       - new Invite
    #       - redirect here
    form = InvitePlayersForm()
    if form.validate_on_submit():
        guestUser = User.query.filter_by(email=form.email.data).first()
        abort = False
        if game.getHostingUser() != current_user:
            flash("Je bent niet de leider van dit spel", "error")
            abort = True
        if form.email.data == current_user.email:
            flash("Je kan niet jezelf uitnodigen...", "error")
            abort = True
        if guestUser == None:
            flash("Deze speler bestaat niet", "error")
            abort = True
        if guestUser in [player.getUser() for player in game.getPlayers()]:
            flash("Deze speler zit al in het spel", "error")
            abort = True
        if Invite.query.filter_by(_user=guestUser, _game=game).first() != None:
            flash("Deze speler is al uitgenodigd", "error")
            abort = True
        
        if abort == False:
            invite = Invite(game=game, user=guestUser)
            db.session.add(invite)
            db.session.commit()
        return redirect(url_for("wakkerdam.game", gameId=game.getId()))


    # Render game.html 
    # @require game{>players, >invites, >host}, form, current_user, chats
    return render_template('wakkerdam/game.html', title=game.getName(), game=game, form=form, current_user=current_user)

@wakkerdam.route('/game/newspaper/<int:newspaperId>', methods=['GET'])
@login_required
def newspaper(newspaperId):
    # Select all papers for this game
    newspaper = Newspaper.query.filter_by(_id=newspaperId).first()

    # @aborts
    #   - newspaper does not exist (hidden)
    #   - player is not in game
    #  @actions
    #   - render newspaper.html

    if newspaper == None:
        flash("Deze krant is niet voor jou", "error")
        return redirect(url_for("wakkerdam.games"))
    if newspaper.getGame() not in [player.getGame() for player in current_user.getPlayers()]:
        flash("Deze krant is niet voor jou", "error")
        return redirect(url_for("wakkerdam.games"))

    return render_template('wakkerdam/newspaper.html', title="De Wakkerdammer", newspaper=newspaper, display_navigation=False)


@wakkerdam.route('/delete-player/<playerId>/<gameId>')
@login_required
def player_delete(playerId, gameId):
    # Select player and game with id's playerId and gameId
    player = Player.query.filter_by(_id=playerId).first()
    game = Game.query.filter_by(_id=gameId).first()

    # @aborts
    #   - player does not exist (hidden)
    #   - game does not exist (hidden)
    #   - game has started
    #   - CU is not host
    #   - player is not in game
    #   - player is CU
    # @actions
    #   - delete player
    #   - redirect wakkerdam.game with gameId
    if game == None or player == None:
        flash("Je zit niet in dit spel", "error")
        return redirect(url_for('wakkerdam.game', gameId=gameId))
    abort = False
    if game.hasStarted():
        flash("Je kan geen spelers meer verwijderen als het spel al is begonnen", "warning")
        abort = True
    if current_user != game.getHostingUser():
        flash("Alleen spelleiders kunnen mensen verwijderen", "error")
        abort = True
    if player not in game.getPlayers():
        flash("Deze speler zit niet in het spel", "error")
        abort = True
    if player == current_user:
        flash("Je kunt niet jezelf verwijderen", "error")
        abort = True
    
    if abort == False:
        db.session.delete(player)
        db.session.commit()
        flash('Speler successvol verwijderd', 'success')

    return redirect(url_for('wakkerdam.game', gameId=gameId))

@wakkerdam.route('/leave/<gameId>')
@login_required
def leave(gameId):
    # Select game with id gameId and player with user CU
    game = Game.query.filter_by(_id=gameId).first()
    player = Player.query.filter_by(_user=current_user).first()

    # @aborts
    #   - game does not exist (hidden)
    #   - current_user not in game
    if game == None:
        flash("Je zit niet in dit spel", "error")
        return redirect(url_for('wakkerdam.game', gameId=gameId))
    abort = False
    if player not in game.getPlayers():
        flash("Deze speler zit niet in het spel", "error")
        abort = True
    
    # @actions
    #   - delete player
    #   - redirect to games
    if abort == False:
        db.session.delete(player)
        db.session.commit()
        flash("Succesvol het spel verlaten", "success")
    
    return redirect(url_for('wakkerdam.games'))


@wakkerdam.route('/new-game', methods=['GET', 'POST'])
@login_required
def new_game():
    # Create new game
    # @aborts
    #   - /
    # @actions
    #   - /

    # Form : CreateGameForm (create new game)
    #   @aborts
    #   - /
    #   @actions
    #   - create game
    #   - create player for current_user
    #   - create village chat
    #   - create chatter for current_user > player in village chat
    #   - redirect to game with new game id
    form = CreateGameForm()
    if form.validate_on_submit():
        game = Game(name=form.name.data, ongoing=1, startDate=form.start_date.data, hostingUser=current_user, playerAmount=form.player_amount.data)
        player = Player(user=current_user, game=game, character=None, isDead=0)
        chatType = ChatType.query.filter_by(_id="1").first()
        chat = Chat(game=game, chatType=chatType)
        chatter = Chatter(player=player, chat=chat)

        db.session.add(game)
        db.session.add(player)
        db.session.add(chat)
        db.session.add(chatter)
        db.session.commit()
        return redirect(url_for('wakkerdam.game', gameId=game.getId()))
    
    # render new-game.html
    # @require form
    return render_template('wakkerdam/new-game.html', form=form)


@wakkerdam.route('/invite')
@login_required
def invite():
    # Select invites for CU
    invites = Invite.query.filter_by(_user=current_user)

    # @aborts
    #   - /

    # Render invite.html
    # @require invite{}
    return render_template('wakkerdam/invite.html', invites=invites)

@wakkerdam.route('/invite/<accept>/<inviteId>')
@login_required
def accept_invite(accept, inviteId):
    # Select invite with id inviteId
    invite = Invite.query.filter_by(_id=inviteId).first()
    
    # @aborts
    #   - invite does not exist (hidden)
    #   - accept is not "accept" or "decline"
    #   - invite not for CU
    #   - game is full for accept is "accept"
    #   - game has started for accept is "accept" 
    #   - already in game for accept is "accept"
    if invite == None:
        flash("Deze invite is niet voor jou", "error")
        return redirect(url_for("wakkerdam.invite"))
    abort = False
    if accept != "accept" and accept != "decline":
        flash(accept +" is geen optie", "error")
        abort = True
    if invite.getUser() != current_user:
        flash("Deze invite is niet voor jou", "error")
        abort = True
    if accept == "accept":
        if len(invite.getGame().getPlayers()) == int(invite.getGame().getPlayerAmount()):
            flash("Dit spel zit al vol", "error")
            abort = True
        if invite.getGame().hasStarted():
            flash("Dit spel is al begonnen", "error")
            abort = True
        if (invite.getUser() in [player.getUser() for player in invite.getGame().getPlayers()]):
            flash("Je zit al in dit spel", "error")
            abort = True

    # @actions
    #   if accept is "accept"
    #       - create player
    #       - create chatter for player in village chat
    #       - delete invite
    #       - redirect to game
    #   if accept is "decline"
    #       - delete invite
    #       - redirect to invite
    if abort == False:
        if accept == "accept":
            player = Player(user=current_user, game=invite.getGame(), character=None, isDead=0)
            villageChatType = chatType = ChatType.query.filter_by(_id="1").first()
            villageChat = Chat.query.filter_by(_game=invite.getGame(), _chatType=villageChatType).first()
            chatter = Chatter(player=player, chat=villageChat)
            db.session.add(player)
            db.session.add(chatter)
            db.session.delete(invite)
            db.session.commit()
            flash("Succesvol toegevoegd aan spel", "success")
            return redirect(url_for("wakkerdam.game", gameId=invite.getGame().getId()))
        elif accept == "decline":
            db.session.delete(invite)
            db.session.commit()
            flash("Uitnodiging succesvol verwijderd", "success")
    return redirect(url_for("wakkerdam.invite"))

@wakkerdam.route('/delete-invite/<inviteId>')
@login_required
def invite_delete(inviteId):
    # Select invite with id inviteId
    invite = Invite.query.filter_by(_id=inviteId).first()

    # @aborts
    #   - invite does not exist
    #   - CU is not host
    if invite == None:
        flash("Deze uitnodiging bestaat niet", "error")
        return redirect(url_for("wakkerdam.games"))
    abort = False
    if invite.getGame().getHostingUser() != current_user:
        flash("Je bent niet de leider van dit spel")
        abort = True

    # @actions
    #   - delete invite
    #   - redirect to wakkerdam.game with gameId invite{>game}
    if abort == False:
        db.session.delete(invite)
        db.session.commit()
        flash("Uitnodiging succesvol verwijderd", "success")
    return redirect(url_for('wakkerdam.game', gameId=invite.getGame().getId()))

@wakkerdam.route('/chat/<chatId>', methods=["GET", "POST"])
@login_required
def chat(chatId):
    # Select chat with id chatId, player with CU and chat's game, chatter with player and chat
    chat = Chat.query.filter_by(_id=chatId).first()
    

    # @aborts
    #   - chat does not exist (hidden)
    #   - player not in game
    #   - player not in chat
    if chat == None:
        flash("Je zit niet in deze chat", "error")
        return redirect(url_for("wakkerdam.games"))
    player = Player.query.filter_by(_user=current_user, _game=chat.getGame()).first()
    if player == None:
        flash("Je zit niet in dit spel", "error")
        return redirect(url_for("wakkerdam.games"))
    chatter = Chatter.query.filter_by(_player=player, _chat=chat).first()
    if chatter == None:
        flash("Je zit niet in deze chat", "error")
        return(redirect(url_for("wakkerdam.game", gameId=chat.getGame().getId())))

    # @actions
    log = ChatLog(chatter=chatter)
    db.session.add(log)

    # Form : NewMessageForm (create new message)
    #   - only for game host
    #   @aborts
    #       - chat is closed
    #   @actions
    #       - new Message
    #       - redirect here
    form = NewMessageForm()
    if form.validate_on_submit():
        if not chat.isOpen():
            flash("Deze chat is dicht, je kan dan geen berichten sturen", "error")
            return redirect(url_for("wakkerdam.chat", chatId=chat.getId()))
        replyTo = form.reply_to.data
        if replyTo == '0':
            replyTo = None
        else:
            replyTo = Message.query.filter_by(_id=replyTo).first()
        message = Message(chatter=chatter, text=form.text.data, replyTo=replyTo)
        db.session.add(message)
        db.session.commit()
        return redirect(url_for("wakkerdam.chat", chatId=chat.getId()))

    db.session.commit()
    # render chat.html
    # @require form, chat{>chatters, >getOnlineAmount(), >getMessages()}
    return render_template("wakkerdam/chat.html", form=form, chat=chat, current_user=current_user, display_navigation=False)

@wakkerdam.route('/delete-message/<messageId>')
def delete_message(messageId):
    # Select message by id
    message = Message.query.filter_by(_id=messageId).first()

    # @aborts
    #   - message does not exist(hidden)
    #   - message is not made by CU
    # @events
    #   - set message to deleted
    #   - redirect to chat
    if message == None:
        flash("Je zit niet in dit spel", "error")
        return redirect('wakkerdam.games')
    if message.getChatter().getPlayer().getUser() != current_user:
        flash("Je kan niet berichten verwijderen die niet door jou zijn geschreven", "error")
        return redirect(url_for('wakkerdam.chat', chatId=message.getChat().getId()))

    message.delete()
    return redirect(url_for('wakkerdam.chat', chatId=message.getChatter().getChat().getId()))

@wakkerdam.route('/karakters')
def characters():
    return render_template('wakkerdam/characters.html')




@wakkerdam.route('/admin_games')
@login_required
@admin_required
def admin_games():
    return "admin all games"
