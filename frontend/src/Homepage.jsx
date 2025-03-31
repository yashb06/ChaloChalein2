// src/Homepage.jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Button, 
  Input, 
  Card, 
  Row, 
  Col, 
  Typography, 
  Tag, 
  Avatar, 
  AutoComplete
} from 'antd';
import { 
  SearchOutlined, 
  EnvironmentOutlined, 
  StarFilled,
  ArrowRightOutlined
} from '@ant-design/icons';

const { Title, Text, Paragraph } = Typography;
const { Meta } = Card;

// Popular destinations data
const popularDestinations = [
  { 
    id: 1, 
    name: 'Paris', 
    image: 'https://images.unsplash.com/photo-1499856871958-5b9627545d1a?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80', 
    description: 'The City of Light awaits with iconic landmarks and charming cafés.'
  },
  { 
    id: 2, 
    name: 'Bali', 
    image: 'https://images.unsplash.com/photo-1537996194471-e657df975ab4?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1738&q=80', 
    description: 'Discover paradise with stunning beaches and vibrant culture.'
  },
  { 
    id: 3, 
    name: 'Tokyo', 
    image: 'https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1488&q=80', 
    description: 'Experience the perfect blend of tradition and innovation.'
  },
  { 
    id: 4, 
    name: 'New York', 
    image: 'https://images.unsplash.com/photo-1496442226666-8d4d0e62e6e9?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1470&q=80', 
    description: 'The city that never sleeps offers endless adventures.'
  }
];

// Travel experiences data
const travelExperiences = [
  {
    id: 1,
    title: 'Cultural Tours',
    icon: '🏛️',
    description: 'Immerse yourself in local traditions and heritage.'
  },
  {
    id: 2,
    title: 'Adventure Activities',
    icon: '🧗',
    description: 'Get your adrenaline pumping with exciting experiences.'
  },
  {
    id: 3,
    title: 'Culinary Journeys',
    icon: '🍽️',
    description: 'Taste the world with authentic local cuisines.'
  },
  {
    id: 4,
    title: 'Relaxation Retreats',
    icon: '🧘',
    description: 'Unwind and rejuvenate at peaceful destinations.'
  }
];

// Testimonials data
const testimonials = [
  {
    id: 1,
    name: 'Sarah Johnson',
    avatar: 'https://randomuser.me/api/portraits/women/44.jpg',
    location: 'London, UK',
    text: 'ChaloChalein made planning my trip to Rome so easy! The AI suggestions were spot on and saved me hours of research.',
    rating: 5
  },
  {
    id: 2,
    name: 'Michael Chen',
    avatar: 'https://randomuser.me/api/portraits/men/32.jpg',
    location: 'Toronto, Canada',
    text: 'I was skeptical about using an AI travel planner, but I was blown away by the personalized itinerary it created for my Japan trip.',
    rating: 5
  },
  {
    id: 3,
    name: 'Priya Sharma',
    avatar: 'https://randomuser.me/api/portraits/women/63.jpg',
    location: 'Mumbai, India',
    text: 'The weather integration was incredibly helpful for packing, and the suggested locations were perfect for my interests!',
    rating: 4
  }
];

const Homepage = () => {
  const navigate = useNavigate();
  const [searchValue, setSearchValue] = useState('');
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);

  // Simulate fetching destination suggestions
  const handleSearch = (value) => {
    setSearchValue(value);
    if (value) {
      setLoading(true);
      // In a real app, this would be an API call
      setTimeout(() => {
        const filteredOptions = ['Paris', 'Tokyo', 'New York', 'Bali', 'Rome', 'Barcelona', 'Sydney']
          .filter(city => city.toLowerCase().includes(value.toLowerCase()))
          .map(city => ({ value: city }));
        setOptions(filteredOptions);
        setLoading(false);
      }, 500);
    } else {
      setOptions([]);
    }
  };

  const startPlanning = (destination = searchValue) => {
    if (destination) {
      // Store the destination in localStorage to use in the chatbot
      localStorage.setItem('selectedDestination', destination);
      navigate('/chatbot');
    }
  };

  return (
    <div className="homepage">
      {/* Hero Section */}
      <div className="hero-section" style={{ 
        backgroundImage: 'url(https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1421&q=80)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        padding: '80px 0',
        position: 'relative'
      }}>
        <div style={{ 
          backgroundColor: 'rgba(0,0,0,0.4)', 
          position: 'absolute', 
          top: 0, 
          left: 0, 
          right: 0, 
          bottom: 0 
        }} />
        
        <div style={{ position: 'relative', zIndex: 1, textAlign: 'center', padding: '0 20px' }}>
          <Title style={{ color: 'white', fontSize: '48px', marginBottom: '24px' }}>
            Discover Your Perfect Journey
          </Title>
          <Paragraph style={{ color: 'white', fontSize: '18px', maxWidth: '800px', margin: '0 auto 40px' }}>
            Let our AI-powered travel assistant create a personalized itinerary based on your preferences and interests.
          </Paragraph>
          
          <div style={{ maxWidth: '700px', margin: '0 auto' }}>
            <AutoComplete
              options={options}
              onSearch={handleSearch}
              onSelect={(value) => setSearchValue(value)}
              style={{ width: '100%' }}
              value={searchValue}
            >
              <Input 
                size="large"
                placeholder="Where would you like to go?" 
                prefix={<EnvironmentOutlined style={{ color: '#1890ff' }} />}
                suffix={
                  <Button 
                    type="primary" 
                    icon={<SearchOutlined />} 
                    onClick={() => startPlanning()}
                    loading={loading}
                  >
                    Plan My Trip
                  </Button>
                }
                onPressEnter={() => startPlanning()}
              />
            </AutoComplete>
          </div>
          
          <div style={{ marginTop: '20px' }}>
            <Text style={{ color: 'white', marginRight: '10px' }}>Popular:</Text>
            {['Paris', 'Bali', 'Tokyo', 'New York'].map(city => (
              <Tag 
                key={city} 
                style={{ cursor: 'pointer', marginRight: '8px', backgroundColor: 'rgba(255,255,255,0.8)' }}
                onClick={() => startPlanning(city)}
              >
                {city}
              </Tag>
            ))}
          </div>
        </div>
      </div>

      {/* How It Works Section */}
      <div style={{ padding: '60px 20px', backgroundColor: '#f5f5f5' }}>
        <Title level={2} style={{ textAlign: 'center', marginBottom: '40px' }}>
          How ChaloChalein Works
        </Title>
        
        <Row gutter={[24, 24]} justify="center" style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <Col xs={24} sm={12} md={6}>
            <Card className="how-it-works-card" bordered={false} style={{ textAlign: 'center', height: '100%' }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>🌍</div>
              <Title level={4}>Choose Your Destination</Title>
              <Text>Tell us where you want to go and when you're planning to travel.</Text>
            </Card>
          </Col>
          
          <Col xs={24} sm={12} md={6}>
            <Card className="how-it-works-card" bordered={false} style={{ textAlign: 'center', height: '100%' }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>✈️</div>
              <Title level={4}>Travel Preferences</Title>
              <Text>Share your interests, travel style, and who you're traveling with.</Text>
            </Card>
          </Col>
          
          <Col xs={24} sm={12} md={6}>
            <Card className="how-it-works-card" bordered={false} style={{ textAlign: 'center', height: '100%' }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>🤖</div>
              <Title level={4}>AI Generates Itinerary</Title>
              <Text>Our AI creates a personalized day-by-day plan just for you.</Text>
            </Card>
          </Col>
          
          <Col xs={24} sm={12} md={6}>
            <Card className="how-it-works-card" bordered={false} style={{ textAlign: 'center', height: '100%' }}>
              <div style={{ fontSize: '48px', marginBottom: '16px' }}>🗺️</div>
              <Title level={4}>Explore & Customize</Title>
              <Text>Review your itinerary, make adjustments, and get ready for your trip!</Text>
            </Card>
          </Col>
        </Row>
      </div>

      {/* Popular Destinations */}
      <div style={{ padding: '60px 20px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '30px' }}>
            <Title level={2} style={{ margin: 0 }}>Popular Destinations</Title>
            <Button type="link" onClick={() => navigate('/chatbot')}>
              View All <ArrowRightOutlined />
            </Button>
          </div>
          
          <Row gutter={[24, 24]}>
            {popularDestinations.map(destination => (
              <Col xs={24} sm={12} md={6} key={destination.id}>
                <Card
                  hoverable
                  cover={<img alt={destination.name} src={destination.image} style={{ height: '200px', objectFit: 'cover' }} />}
                  onClick={() => startPlanning(destination.name)}
                >
                  <Meta 
                    title={destination.name} 
                    description={destination.description} 
                  />
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      </div>

      {/* Travel Experiences */}
      <div style={{ padding: '60px 20px', backgroundColor: '#f5f5f5' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <Title level={2} style={{ textAlign: 'center', marginBottom: '40px' }}>
            Discover Experiences
          </Title>
          
          <Row gutter={[24, 24]}>
            {travelExperiences.map(experience => (
              <Col xs={24} sm={12} md={6} key={experience.id}>
                <Card bordered={false} style={{ textAlign: 'center', height: '100%' }}>
                  <div style={{ fontSize: '48px', marginBottom: '16px' }}>{experience.icon}</div>
                  <Title level={4}>{experience.title}</Title>
                  <Text>{experience.description}</Text>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      </div>

      {/* Testimonials */}
      <div style={{ padding: '60px 20px' }}>
        <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
          <Title level={2} style={{ textAlign: 'center', marginBottom: '40px' }}>
            What Our Travelers Say
          </Title>
          
          <Row gutter={[24, 24]}>
            {testimonials.map(testimonial => (
              <Col xs={24} md={8} key={testimonial.id}>
                <Card bordered={false} style={{ height: '100%' }}>
                  <div style={{ display: 'flex', alignItems: 'center', marginBottom: '16px' }}>
                    <Avatar size={64} src={testimonial.avatar} />
                    <div style={{ marginLeft: '16px' }}>
                      <Title level={5} style={{ margin: 0 }}>{testimonial.name}</Title>
                      <Text type="secondary">{testimonial.location}</Text>
                      <div>
                        {[...Array(5)].map((_, i) => (
                          <StarFilled 
                            key={i} 
                            style={{ 
                              color: i < testimonial.rating ? '#FADB14' : '#E8E8E8',
                              marginRight: '4px'
                            }} 
                          />
                        ))}
                      </div>
                    </div>
                  </div>
                  <Paragraph style={{ fontSize: '16px' }}>"{testimonial.text}"</Paragraph>
                </Card>
              </Col>
            ))}
          </Row>
        </div>
      </div>

      {/* CTA Section */}
      <div style={{ 
        padding: '80px 20px', 
        backgroundImage: 'linear-gradient(to right, #1890ff, #096dd9)',
        textAlign: 'center'
      }}>
        <Title level={2} style={{ color: 'white', marginBottom: '24px' }}>
          Ready to Plan Your Dream Vacation?
        </Title>
        <Paragraph style={{ color: 'white', fontSize: '18px', maxWidth: '700px', margin: '0 auto 32px' }}>
          Let our AI travel assistant create a personalized itinerary based on your preferences. No more hours of research!
        </Paragraph>
        <Button 
          type="primary" 
          size="large"
          style={{ backgroundColor: 'white', color: '#1890ff', borderColor: 'white', height: '50px', fontSize: '16px', fontWeight: 'bold' }}
          onClick={() => navigate('/chatbot')}
        >
          Start Planning Now
        </Button>
      </div>

      <style jsx>{`
        .homepage {
          font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .how-it-works-card:hover {
          transform: translateY(-5px);
          box-shadow: 0 8px 16px rgba(0,0,0,0.1);
          transition: all 0.3s ease;
        }
      `}</style>
    </div>
  );
};

export default Homepage;