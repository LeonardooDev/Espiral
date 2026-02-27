Este es el código fuente de "Espiral", hasta el momento es simple pero se le agregarán nuevas cosas pronto.

La idea de Espiral es hacer un controlador con Inteligencia Artificial integrada. Controlador en el aspecto de que si yo en mi computadora digo "quiero abrir un documento", Espiral se encargue de abrirlo; si quiero mandar un mensaje, que solo con decirlo se abra mi app de mensajería. La idea en general es un controlador que sepa lo que quieres.

La arquitectura que tengo pensada es: tú dices "quiero un documento", tu voz se transforma a texto, ese texto se envía a la IA, la IA observa tu petición y entiende qué quieres. Al darse cuenta de que buscas un documento, manda un JSON diciendo que lo que el usuario busca es una acción llamada "documento". En el código ya está escrito qué hacer en cada caso: con el nombre "documento", el código tiene las instrucciones de buscar Word; si lo encuentra lo abre, y si no, busca programas parecidos de edición.

Eso no es todo, la IA puede hacer preguntas más específicas para conocer qué quieres, como: "¿Quieres un archivo de texto o una presentación?". Esto ayuda a que la IA clasifique mejor la petición del usuario.

¡CAMBIO DE PLANES!:
Originalmente pensé en usar una IA online por las complicaciones del peso y la implementación. Pero para este proyecto hemos decidido ir un paso más allá: TODO ES 100% OFFLINE.

¿Por qué? Porque ganar un concurso con una IA que depende de internet es fácil, pero hacer que una computadora razone, entienda y controle el sistema sin cables y sin conexión es lo que marca la diferencia. Espiral ahora corre localmente usando Ollama, lo que garantiza privacidad.

Lo que también es offline es la característica de texto a voz (TTS). El código está pensado para que funcione incluso en dispositivos algo viejos. Aunque se sacrifique un poco la calidad de la voz "perfecta" de las nubes de pago, ganamos un sistema que siempre está activo, sin trabas y sin límites de uso.

Ya está implementada la característica de voz a texto. Se puede hablar con la IA por terminal, pero la meta final es que la IA razone las consultas y solo interactúe con el usuario si es estrictamente necesario para ejecutar la acción.
