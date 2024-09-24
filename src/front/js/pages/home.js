import React, { useContext } from "react";
import { Context } from "../store/appContext";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";

export const Home = () => {
	const { store, actions } = useContext(Context);

	return (
		<div className="big-one-container">
			<div className="contiainer text-center box-container-header">
				<div className="content-box">
					<div className="col-12">
						<h1 className="display-4">Bienvenido a Cafe Canaima</h1>
						<p className="lead">
							Descubre nuestros deliciosos productos y disfruta de un café excepcional en un ambiente acogedor.
						</p>
					</div>
				</div>
			</div>
		</div>
	);
};

