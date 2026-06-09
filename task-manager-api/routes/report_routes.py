from flask import Blueprint
from controllers.report_controller import ReportController

report_bp = Blueprint('reports', __name__)

@report_bp.route('/reports/summary', methods=['GET'])
def summary_report():
    return ReportController.summary_report()

@report_bp.route('/reports/user/<int:user_id>', methods=['GET'])
def user_report(user_id):
    return ReportController.user_report(user_id)

@report_bp.route('/categories', methods=['GET'])
def get_categories():
    return ReportController.get_categories()

@report_bp.route('/categories', methods=['POST'])
def create_category():
    return ReportController.create_category()

@report_bp.route('/categories/<int:cat_id>', methods=['PUT'])
def update_category(cat_id):
    return ReportController.update_category(cat_id)

@report_bp.route('/categories/<int:cat_id>', methods=['DELETE'])
def delete_category(cat_id):
    return ReportController.delete_category(cat_id)
