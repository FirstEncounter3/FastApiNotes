import { useState, useEffect } from "react";

import CreateNote from "../CreateNote/CreateNote";

const Notes = () => {
    const [notes, setNotes] = useState([]);

    const get_notes_url = "http://127.0.0.1:8000/api/v1/notes"

    const fetchNotes = async () => {
        try {
            const response = await fetch(get_notes_url);
            const data = await response.json();
            setNotes(data);
        }
        catch (error) {
            console.log(error);
        }
    }

    useEffect(() => {
        fetchNotes();
    }, []);


    return (
        <div>
            <h1>Notes</h1>
            {notes.length > 0 ? (
                <ul>
                    {notes.map((note) => (
                        <li key={note.id}>{note.title}
                            <p>{note.content}</p>
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No notes found</p>
            )}
            <CreateNote onNoteCreated={fetchNotes}/>
        </div>
        
    )
}

export default Notes;