from snippet_manager.repository import create_snippet, exists_same_title_lang, get_snippet_by_id, update_snippet
from snippet_manager.utils import normalize_tags, now_iso


def add_snippet(title,language,category, tags, content):
    if not title or not title.strip():
        raise ValueError("Il titolo è obbligatorio.")
    if not content or not content.strip():
        raise ValueError("Il contenuto è obbligatorio.")
    
    tags_norm=normalize_tags(tags)
    if exists_same_title_lang(title,language):
        raise ValueError("Esiste già uno snippet con lo stesso titolo per questo linguaggio.")
    
    ts=now_iso()
    favorite=0
    snippet_data={'title':title,'language':language,'category':category,
          'tags':tags_norm,'content':content,'favorite':favorite,'created_at':ts,'updated_at':ts}
    id=create_snippet(snippet_data)

    return id

def edit_snippet(id, title=None, language=None, category=None, tags=None, content=None):
    row=get_snippet_by_id(id)
    if row is None:
        raise ValueError('Snippet non trovato')
    
    update_data={}
    if title is not None and title.strip()!='':
        update_data['title']=title
    if language is not None and language.strip()!='':
        update_data['language']=language.lower()
    if category is not None and category.strip()!='':
        update_data['category']=category.lower()
    if tags is not None and tags.strip()!='':
        update_data['tags']=normalize_tags(tags)
    if content is not None:
        if content.strip()=='':
            raise ValueError('Il contenuto non può essere vuoto')
        else:
            update_data['content']=content
    update_data['updated_at']=now_iso()
    if not update_data:
        return 0

    righe_mod=update_snippet(id,update_data)

    return righe_mod        
                       
