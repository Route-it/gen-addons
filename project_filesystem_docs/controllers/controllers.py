# -*- coding: utf-8 -*-
from openerp import http

# class ProjectFilesystemDocs(http.Controller):
#     @http.route('/project_filesystem_docs/project_filesystem_docs/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/project_filesystem_docs/project_filesystem_docs/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('project_filesystem_docs.listing', {
#             'root': '/project_filesystem_docs/project_filesystem_docs',
#             'objects': http.request.env['project_filesystem_docs.project_filesystem_docs'].search([]),
#         })

#     @http.route('/project_filesystem_docs/project_filesystem_docs/objects/<model("project_filesystem_docs.project_filesystem_docs"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('project_filesystem_docs.object', {
#             'object': obj
#         })