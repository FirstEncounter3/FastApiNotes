import { useState } from "react";

const CreateNote = ({ onNoteCreated }) => {

    const create_note_url = "http://127.0.0.1:8000/api/v1/create_notes"
    const [title, setTitle] = useState('');
    const [content, setContent] = useState('');

    const handleFormSubmit = async (e) => {
        e.preventDefault();
        const body = {title, content}
        try {
            const response = await fetch(create_note_url, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            const data = await response.json();
            console.log(data);
        } catch (error) {
            console.error(error);
        }
        onNoteCreated();
        setTitle('');
        setContent('');
    };


    return (
        <div>
            <label htmlFor="title">Title:</label>
            <input type="text" id="title" value={title} onChange={(e) => setTitle(e.target.value)} />
            <label htmlFor="content">Content:</label>
            <textarea id="content" value={content} onChange={(e) => setContent(e.target.value)} />
            <button type="submit" onClick={handleFormSubmit}>Create Note</button>
        </div>
    )

};

export default CreateNote;