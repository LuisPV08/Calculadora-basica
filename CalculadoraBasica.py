import tkinter as tk
from tkinter import messagebox

class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora")
        
        # Variables de estado
        self.numero_actual = "0"
        self.primer_numero = None
        self.operacion = None
        self.nuevo_numero = True
        self.expresion = ""
        
        # Crear y configurar el display
        self.display = tk.Entry(root, justify="right", font=('Arial', 20))
        self.display.grid(row=0, column=0, columnspan=4, padx=5, pady=5, sticky="nsew")
        self.display.insert(0, "0")
        self.display.config(state="disabled")
        
        # Configurar el grid
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        
        # Definir botones
        botones = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            'C', '0', '=', '+'
        ]
        
        # Crear y posicionar botones
        row = 1
        col = 0
        for boton in botones:
            cmd = lambda x=boton: self.click_boton(x)
            texto_boton = boton
            if boton == '*': texto_boton = '×'
            if boton == '/': texto_boton = '÷'
            btn = tk.Button(root, text=texto_boton, command=cmd, font=('Arial', 15))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            col += 1
            if col > 3:
                col = 0
                row += 1
    
    def actualizar_display(self, texto):
        """Actualiza el texto mostrado en el display"""
        self.display.config(state="normal")
        self.display.delete(0, tk.END)
        self.display.insert(0, texto)
        self.display.config(state="disabled")
    
    def click_boton(self, valor):
        """Maneja los clicks en los botones"""
        if valor.isdigit():
            if self.nuevo_numero:
                self.numero_actual = valor
                self.nuevo_numero = False
                # Si no hay operación previa, comenzar nueva expresión
                if not self.operacion:
                    self.expresion = valor
                else:
                    # Si hay operación, mantener la expresión y agregar el nuevo número
                    self.expresion = self.expresion + valor
            else:
                self.numero_actual += valor
                self.expresion = self.expresion + valor
            self.actualizar_display(self.expresion)
            
        elif valor in "+-*/":
            if self.numero_actual:
                if self.primer_numero is not None and not self.nuevo_numero:
                    self.calcular()
                self.operacion = valor
                self.primer_numero = float(self.numero_actual)
                self.nuevo_numero = True
                operador_display = '×' if valor == '*' else '÷' if valor == '/' else valor
                self.expresion = f"{self.numero_actual} {operador_display} "
                self.actualizar_display(self.expresion)
                
        elif valor == "=":
            if self.operacion and self.primer_numero is not None and self.numero_actual:
                self.calcular()
                self.actualizar_display(self.numero_actual)
                self.expresion = self.numero_actual
                self.primer_numero = None
                self.operacion = None
                
        elif valor == "C":
            self.limpiar()
    
    def calcular(self):
        """Realiza el cálculo basado en la operación seleccionada"""
        try:
            segundo_numero = float(self.numero_actual)
            if self.operacion == "+":
                resultado = self.primer_numero + segundo_numero
            elif self.operacion == "-":
                resultado = self.primer_numero - segundo_numero
            elif self.operacion == "*":
                resultado = self.primer_numero * segundo_numero
            elif self.operacion == "/":
                if segundo_numero == 0:
                    messagebox.showerror("Error", "No se puede dividir por cero")
                    self.limpiar()
                    return
                resultado = self.primer_numero / segundo_numero
            
            # Formatear resultado para evitar decimales innecesarios
            if isinstance(resultado, float) and resultado.is_integer():
                resultado = int(resultado)
            
            self.numero_actual = str(resultado)
            self.nuevo_numero = True
            
        except Exception as e:
            messagebox.showerror("Error", "Error en el cálculo")
            self.limpiar()
    
    def limpiar(self):
        """Reinicia la calculadora"""
        self.numero_actual = "0"
        self.primer_numero = None
        self.operacion = None
        self.nuevo_numero = True
        self.expresion = ""
        self.actualizar_display("0")

def main():
    root = tk.Tk()
    root.geometry("300x400")
    app = Calculadora(root)
    root.mainloop()

if __name__ == "__main__":
    main()