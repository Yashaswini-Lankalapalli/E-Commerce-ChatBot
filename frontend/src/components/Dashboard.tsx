import React from 'react';
import { useSelector } from 'react-redux';
import {
  Box,
  Container,
  Typography,
  Grid,
  Paper,
  Button,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { RootState } from '../store';

const Dashboard: React.FC = () => {
  const { user } = useSelector((state: RootState) => state.auth);
  const navigate = useNavigate();

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Welcome Section */}
        <Grid item xs={12}>
          <Paper
            sx={{
              p: 3,
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              textAlign: 'center',
            }}
          >
            <Typography variant="h4" component="h1" gutterBottom>
              Welcome, {user?.name}!
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Explore our products and get assistance from our AI-powered chatbot.
            </Typography>
            <Button
              variant="contained"
              color="primary"
              size="large"
              onClick={() => navigate('/products')}
              sx={{ mt: 2 }}
            >
              Browse Products
            </Button>
          </Paper>
        </Grid>

        {/* Features Section */}
        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              textAlign: 'center',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Smart Search
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Find products quickly with our advanced search functionality and AI-powered recommendations.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              textAlign: 'center',
            }}
          >
            <Typography variant="h6" gutterBottom>
              AI Assistant
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Get instant help from our chatbot for product information, order status, and more.
            </Typography>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper
            sx={{
              p: 3,
              height: '100%',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              textAlign: 'center',
            }}
          >
            <Typography variant="h6" gutterBottom>
              Secure Shopping
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Shop with confidence with our secure payment system and data protection.
            </Typography>
          </Paper>
        </Grid>

        {/* Quick Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Quick Actions
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
              <Button
                variant="outlined"
                onClick={() => navigate('/products')}
              >
                View All Products
              </Button>
              <Button
                variant="outlined"
                onClick={() => {
                  // Scroll to chatbot
                  const chatbot = document.querySelector('.chatbot-container');
                  chatbot?.scrollIntoView({ behavior: 'smooth' });
                }}
              >
                Open Chat Assistant
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Dashboard; 