import React from 'react';
import {CKEditor} from "@ckeditor/ckeditor5-react";
import Editor from "ckeditor5-custom-build";

const TaskEditor = () => {
    return (
        <CKEditor
            editor={Editor}
            data={'Описание задачи'}
            onChange={(event, editor) => {
                const data = editor.getData();
                console.log({event, editor, data});
            }}

        />
    )
};

export default TaskEditor;