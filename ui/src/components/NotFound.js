/*
2023-02-20
ui/src/components/NotFound.js

*/

import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button, CardContent, CardHeader } from '@mui/material';

import BasicCard from '../components/common/BasicCard/BasicCard';
import GridWrapper from './common/GridWrapper/GridWrapper';
import PageHeader from './Page/PageHeader';

const NoMatch = () => {
    let navigate = useNavigate();
    return (
        <>
            <PageHeader title="Nothing to see here!"></PageHeader>
            <GridWrapper>
                <BasicCard>
                    <CardHeader title='404' subheader='Page Not Found' />
                    <CardContent>
                        <Button variant='contained' onClick={() => {navigate('/')}}>Go Back To Stream</Button>
                    </CardContent>
                </BasicCard>
            </GridWrapper>
        </>
    );
}

export default NoMatch;
