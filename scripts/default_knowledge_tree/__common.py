def insert_tree(db, model, tree, parent=None):
    for name, children in tree.items():
        new_record = model(name=name, parent_id=parent.id if parent is not None else None)
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        
        if children:
            insert_tree(db, model, children, new_record)
