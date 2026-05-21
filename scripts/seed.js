const mongoose = require('mongoose');
require('dotenv').config();

const Home = require('../models/Home');
const Content = require('../models/Content');
const SacredSpace = require('../models/SacredSpace');

const seedData = async () => {
  try {
    await mongoose.connect(process.env.MONGODB_URI);
    console.log('✅ Connected to MongoDB');

    // Limpiar datos existentes
    await Home.deleteMany({});
    await Content.deleteMany({});
    await SacredSpace.deleteMany({});

    // Crear datos iniciales para Home
    const home = new Home({
      title: 'Manifestation Journal',
      subtitle: 'Tu espacio para rituales, intenciones y crecimiento personal',
      description: 'Un diario sagrado donde tus intenciones cobran vida. Registra rituales, manifestaciones y observa tu crecimiento energético.',
      tagline: 'Manifiesta tu realidad, cultiva tu energía',
    });
    await home.save();
    console.log('✅ Home data seeded');

    // Crear contenidos de Growth
    const growthContents = [
      {
        title: 'Meditación Matutina',
        description: 'Comienza tu día con claridad y propósito',
        category: 'meditation',
        content: 'Siéntate en un lugar tranquilo. Inhala profundamente durante 4 segundos, mantén por 4, exhala por 4. Repite 10 veces.',
        author: 'Manifestation Journal',
        difficulty: 'beginner',
        duration: 10,
      },
      {
        title: 'Ritual de Abundancia',
        description: 'Atraer prosperidad a tu vida',
        category: 'ritual',
        content: 'Enciende una vela blanca. Escribe en papel lo que deseas atraer. Lee en voz alta 3 veces. Quema el papel en la vela.',
        author: 'Manifestation Journal',
        difficulty: 'beginner',
        duration: 15,
      },
      {
        title: 'Afirmaciones Diarias',
        description: 'Reprogramar tu mente para el éxito',
        category: 'affirmation',
        content: 'Soy capaz. Soy fuerte. Soy digno. Mis sueños se hacen realidad. Atraigo lo que deseo.',
        author: 'Manifestation Journal',
        difficulty: 'beginner',
        duration: 5,
      },
      {
        title: 'Práctica de Gratitud',
        description: 'Elevar tu vibración con gratitud',
        category: 'practice',
        content: 'Anota 5 cosas por las que estés agradecido. Siéntelo en tu cuerpo. Visualiza cómo estas cosas te hacen feliz.',
        author: 'Manifestation Journal',
        difficulty: 'beginner',
        duration: 10,
      },
      {
        title: 'Baño Energético',
        description: 'Purificación y renovación',
        category: 'ritual',
        content: 'Añade sal marina y pétalos de rosa al agua. Visualiza una luz dorada limpiando tu aura.',
        author: 'Manifestation Journal',
        difficulty: 'intermediate',
        duration: 20,
      },
    ];
    await Content.insertMany(growthContents);
    console.log('✅ Growth content seeded');

    // Crear espacios sagrados
    const sacredSpaces = [
      {
        title: 'Santuario de Calma',
        description: 'Un espacio para la tranquilidad interior',
        content: 'Imagina una habitación con luz dorada suave. Las paredes son de mármol blanco. Hay flores blancas por todas partes. El aire huele a lavanda. Aquí estás segura y en paz.',
        ambiance: 'calm',
      },
      {
        title: 'Montaña Sagrada',
        description: 'Conexión con tu poder interior',
        content: 'Estás en la cima de una montaña. El cielo es de un azul profundo. Sientes el viento en tu rostro. Desde aquí puedes ver el futuro que deseas crear.',
        ambiance: 'grounding',
      },
      {
        title: 'Jardín de Energía',
        description: 'Lugar de renovación y crecimiento',
        content: 'Un jardín infinito lleno de flores de todos los colores. Cristales brillan en el suelo. La energía fluye a través de ti. Aquí todo es posible.',
        ambiance: 'energizing',
      },
      {
        title: 'Templo de Equilibrio',
        description: 'Armonía entre cuerpo, mente y espíritu',
        content: 'Un templo antiguo de piedra blanca. La luz natural entra por grandes ventanas. Todo está en perfecto equilibrio. Sientes paz y poder simultáneamente.',
        ambiance: 'balancing',
      },
    ];
    await SacredSpace.insertMany(sacredSpaces);
    console.log('✅ Sacred spaces seeded');

    console.log('🌟 Database successfully seeded!');
    process.exit(0);
  } catch (error) {
    console.error('❌ Error seeding database:', error);
    process.exit(1);
  }
};

seedData();
