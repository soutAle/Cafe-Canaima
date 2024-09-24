import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/footer.css';

export const Footer = () => {
    return (
        <footer className="footer text-center text-lg-start">
            <div className="container p-4">
                <div className="row">
                    <div className="col-lg-4 col-md-6 mb-4 mb-md-0">
                        <h5 className="text-uppercase">Sobre Nosotros</h5>
                        <p>
                            Cafe Canaima es un lugar donde puedes disfrutar de las mejores bebidas y comidas
                            en un ambiente acogedor. Te invitamos a visitarnos.
                        </p>
                    </div>
                    <div className="col-lg-4 col-md-6 mb-4 mb-md-0">
                        <h5 className="text-uppercase">Enlaces Rápidos</h5>
                        <ul className="list-unstyled">
                            <li>
                                <Link to="/" className="text-dark">Inicio</Link>
                            </li>
                            <li>
                                <Link to="/products" className="text-dark">Productos</Link>
                            </li>
                            <li>
                                <Link to="/services" className="text-dark">Servicios</Link>
                            </li>
                            <li>
                                <Link to="/contact" className="text-dark">Contactar</Link>
                            </li>
                        </ul>
                    </div>
                    <div className="col-lg-4 col-md-6 mb-4 mb-md-0">
                        <h5 className="text-uppercase">Síguenos</h5>
                        <ul className="list-unstyled">
                            <li>
                                <a href="https://www.facebook.com" target="_blank" rel="noopener noreferrer" className="text-dark">Facebook</a>
                            </li>
                            <li>
                                <a href="https://www.instagram.com" target="_blank" rel="noopener noreferrer" className="text-dark">Instagram</a>
                            </li>
                            <li>
                                <a href="https://www.twitter.com" target="_blank" rel="noopener noreferrer" className="text-dark">Twitter</a>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
            <div className="text-center p-3 bg-dark text-white">
                © 2024 Cafe Canaima. Todos los derechos reservados.
            </div>
        </footer>
    );
};

