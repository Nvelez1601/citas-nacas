import { useMemo } from "react";
import Particles from "react-tsparticles";
import { loadFull } from "tsparticles";

import lilyUrl from "../assets/lily.svg";

export default function LilyParticles() {
  const options = useMemo(
    () => ({
      fullScreen: { enable: false },
      fpsLimit: 30,
      particles: {
        number: { value: 18, density: { enable: true, area: 900 } },
        move: {
          direction: "top",
          speed: 0.4,
          outModes: { default: "out" }
        },
        opacity: { value: 0.35 },
        size: { value: { min: 18, max: 44 } },
        shape: {
          type: "image",
          image: [{ src: lilyUrl, width: 120, height: 120 }]
        }
      },
      interactivity: {
        events: {
          onHover: { enable: false },
          onClick: { enable: false }
        }
      },
      detectRetina: true
    }),
    []
  );

  const particlesInit = async (engine) => {
    await loadFull(engine);
  };

  return (
    <Particles
      id="lily-particles"
      init={particlesInit}
      options={options}
      className="absolute inset-0 -z-10"
    />
  );
}
