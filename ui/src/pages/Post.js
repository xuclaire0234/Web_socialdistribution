import React from 'react';
import { useNavigate } from 'react-router-dom';

const Post = () => {
    let navigate = useNavigate();

    return (
        <>
            <div>
                Place holder for post
            </div>

            <button onClick={() => {
                navigate(-1)
            }}>
                go back to stream
            </button>
        </>
    );
}

export default Post;