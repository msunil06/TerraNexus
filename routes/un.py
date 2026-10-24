from flask import Blueprint, render_template
from services.un_service import UNService

un_bp = Blueprint("un", __name__, url_prefix="/un")

@un_bp.route("", strict_slashes=False)
@un_bp.route("/", strict_slashes=False)
def index():
    overview = UNService.get_un_overview()
    p5_members = UNService.get_p5_permanent_members()
    temp_members = UNService.get_temporary_security_council_members()
    agencies = UNService.get_specialized_agencies()
    peacekeeping = UNService.get_peacekeeping_missions()

    return render_template(
        "un/index.html",
        overview=overview,
        p5_members=p5_members,
        temp_members=temp_members,
        agencies=agencies,
        peacekeeping=peacekeeping
    )
