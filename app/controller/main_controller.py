from flask import Blueprint, render_template

from app.utils.decorators import login_required

main_bp = Blueprint('main', __name__, url_prefix='/')


@main_bp.route('/', methods=['GET'])
@login_required
def index():
    """
    displaying main page

    Returns:
        str: main page
    """

    return render_template('index.html')
