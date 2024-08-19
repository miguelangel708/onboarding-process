from models.validateActions import validateActions

document_validation = True
country = "CO"
doc_type = "identity-card"
accept_terms = True

validate_actions = validateActions(document_validation, country, doc_type, accept_terms)
validate_actions.pipeline_document_validation()
    
