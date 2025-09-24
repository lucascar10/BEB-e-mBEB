# Neste programa há tanto o método BEB quanto o mBEB, de modo que o usuário pode escolher qual deseja usar.
# Script - mBEB surge como modificação do Script BEB já feito. Aqui iremos implementar o termo de energia de aparecimento dos íons.
from math import pi, log, isclose

# Definindo constantes: (Fonte - NIST)

a = 0.529177210544 # Aqui a resposta será dada em 10^-20 m^2, devido a unidade do raio de Bohr.
R = 13.61   # Energia de Rydberg em eV

# Escolha o método computacional a ser feito.
nome = ''
passo = 0.0
nome_BR = ''
while True:
    print(f'{'-'*80}')
    print('Escolha o método computacional a ser calculado:')
    print('[0] - BEB: Cálculo da seção de choque total de ionização.\n[1] - mBEB: Cálculo da seção de choque parcial de ionização.')
    #controle = input('Digite sua escolha: ').lower()
    print(f'{'-'*80}')
    controle = input('Digite a opção desejada: ')
    if controle not in '10':
        print('Opção inválida. Por favor, tente novamente.')
    else:
        if controle == '0':
            print('Prosseguindo para o método BEB...')
            #nome = input('Digite o nome do arquivo com os dados do Gaussian 03: ')
            nome = input('Digite o nome do arquivo com os dados do Gaussian 03: ')
            #passo = float(input('Digite o passo na energia (em eV): '))
            passo = float(input('Digite o passo na energia (em eV): '))
        
        else:
            print('Prosseguindo para o método mBEB..')
            #nome = input('Digite o nome do arquivo com os dados do Gaussian 03: ')
            nome = input('Digite o nome do arquivo com os dados do Gaussian 03: ')
            #passo = float(input('Digite o passo na energia (em eV): '))
            passo = float(input('Digite o passo na energia (em eV): '))
            #nome_BR = input('Digite o nome do arquivo que contém os Branching Ratio da molécula selecionada: ')
            nome_BR = input('Digite o nome do arquivo com os dados do branching ratio da molécula escolhida: ')
        break

# Lendo arquivos:
    # Lendo arquivo  com dados do Gaussian 03:
with open(f"{nome}.txt", "r") as dados_G03:
    dados= dados_G03.readlines()

    # Lendo arquivo com os dados do Branching Ratio:
if controle == '1':
    with open(f"{nome_BR}.txt", "r") as dados_BR:
        arquivo_BR = dados_BR.readlines()
# Aqui, temos que os dados relevantes para os futuros cálculos foram lidos e salvos como variáveis na memória do computador. 
    # A variável 'dados' contém informações sobre as energias de ligação e cinética média dos elétrons nos orbitais moleculares.
    # A variável 'arquivo_BR' contém informações sobre as razões massa/carga, branching ratio (provenientes do NIST) e energia de aparecimento de fragmentos iônicos possíveis da molécula de estudo.

# Agora iremos criar as listas, objetos passíveis de serem acessados, com as informações relevantes para os métodos.

valores = []
# Esta lista, 'valores', foi criada como passo intermediário para criação de duas novas listas que dizem respeito às energias associadas a um único orbital.
for i in dados:
    valores.append(i.split())

valores_BR = []
# Esta lista, 'valores_BR', foi criada como passo intermediário para a criação de novas listas que dizem respeito aos fragmentos iônicos da moléculas em estudo.
for i in arquivo_BR:
    valores_BR.append(i.split())

# Agora criamos, de fato, as listas com as energias potenciais e cinética média dos elétrons nos orbitais.
potencial = []
cinetica = []
for i in range (len(valores)):
    # Devemos transformar as energias obtidas pelos cálculos HF, que são dadas em unidades de Hartree para valores em eV.
    # Deste modo, multiplicamos os valores por 27.2114, já que 1 Hartree = 27.2114 eV.
    potencial.append(float(valores[i][0])*27.2114)
    cinetica.append(float(valores[i][1])*27.2114)

# Encontrando energia de Ionização da Molécula.
EI = potencial[0]
for j in range (len(potencial)):
    if EI >= potencial[j]:
        EI = potencial[j]

# Agora criamos as listas com os valores relativos a cada fragmento que pode ser gerado por conta da ionização.
BR = []
razao_MQ = []
energia_aparecimento = []
for i in range (len(valores_BR)):
    # Criando três listas, uma com as razões massa/carga e outra com os branching e última com as energias de aparecimento dos fragmentos.
    var = valores_BR[i][2]
    # Nesta notação o valor '0' em energia de aparecimento denota o íon "pai" e '-' denota íons com energias de aparecimento indisponíveis.
     # Caso encontremos a string '0', sabemos que estamos tratando do íon pai.
        # Assim, a energia de aparecimento deste íon e a energia de ligação do elétron mais fracamente ligado.
            # Isto é, do orbital com menor valor de energia de ligação. Assim, procuramos o menor valor de energia de ligação e atribuimos como energia de aparecimento do íon pai.
    if var == '0':
        var = potencial [0]
        for j in range (len(potencial)):
            if var >= potencial[j]:
                var = potencial[j]
    elif var == '0+':
        var = potencial [0]
        for j in range (len(potencial)):
            if var >= potencial[j]:
                var = potencial[j]
    # Aqui, devemos eliminar fragmentos com energias de aparecimento indisponíveis
    try:
    # Tentamos transformar e guardar os valores para as energias de aparecimento em números e tratamos as exceções.
        energia_aparecimento.append(float(var))
    # Tratando as exceções:
    except:
    # Caso não tenhamos a informação da energia de aparecimento, não salvamos nenhum parâmetro referente a tal fragmento.
        continue
   
    # Por fim, criamos a lista com as energias de aparecimento dos íons que serão trabalhados e porteriormente, criamos as listas que contém as razões massa/carga e os branching ratio (BR) de tais fragmentos.
    razao_MQ.append(int(valores_BR[i][0]))
    BR.append(float(valores_BR[i][1]))


# Agora com as quantidades devidamente definidas e salvas, iremos começar os cálculos:
    # Como em ambos os contextos realizaremos o uso de quantidades obtidas no BEB, começamos fazendo-o então:

# Faremos duas somatórias, a primeira será com respeito aos orbitais moléculares e a segunda será com respeito ao range de energia (faremos de 0 a 10000 eV, como Leonardo, em seu código em Fortran77).
# Definindo quantidades: * Todas as quantidades do método BEB terá algum indicativo no nome (BEB ou total)*.

Q_total_70eV = 0
# A variável 'Q_total_70eV' é de extrema importância para o cálculo mBEB.
total_cross_section = []
# A lista 'total_cross_section' representa a seção de choque total de ionização para uma nada energia.
energia_BEB = []
# A lista 'energia_BEB' está associada a energia do elétron incidente.
E = 0.0
# Realizando, finalmente, os cálculos:
while E <= 10000 + passo:
    # Neste for, E representa a energia do elétron incidente.
    # Notavelmente, se o elétron incidente tem energia 0, a seção de choque é nula
    SCTI = 0
    for j in range (len(potencial)):
    # Já neste for, j representa o j-ésimo orbital.
        B = potencial[j]
        scti_orbital_j = 0
        t_BEB = E/B
        if t_BEB > 1.0:
            U =cinetica[j]
            u = U/B
            S = 8*pi*(a**2)*((R/B)**2)
            # Calculando SCTI pelo método BEB: *Utilizaremos a equação simplificada (Q=1)*
            # Separando os termos da fórmula:
            # 1° termo:
            term1 = 0.5*log(t_BEB)*(1-t_BEB**-2)
            # 2° termo:
            term2 = 1-1/t_BEB
            # 3° termo:
            term3 = log(t_BEB)/(t_BEB+1)
            # Seção de choque do j-ésimo orbital para esta energia i:
            scti_orbital_j = (S/(1+t_BEB+u))*(term1 + term2 - term3)
        SCTI += scti_orbital_j
    # Então, somamos todas as contribuições dos orbitais e temos a SCTI para tal energia.
    total_cross_section.append(SCTI)
    # Assim, finalmente podemos computar o valor de energia E, para o qual a SCTI foi calculada e passar para a próxima.
    energia_BEB.append(E)
    # Aqui, ao chegarmos no valor de 70 eV, reservamos o valor da SCTI. Importanto para o mBEB.
    if isclose(E, 70.0):
        Q_total_70eV = SCTI
        print(f'SCTI 70 eV: {Q_total_70eV}') 
    E += passo

# Finalmente terminado os procedimentos relativos ao método BEB, podemos criar o arquivo txt com os resultados obtidos e salvar a informação importante ao mBEB.
    # Como, para o método mBEB precisamos determinar o fator gamma a uma certa energia e, para tanto, precisamos da seção de choque total nesta mesma energia fornecida pelo BEB.
        #Podemos guardar esta informação neste momento de escrita de valores num txt.

# Criando arquivo txt com as seções de choque total para todas as energias.

with open(f"{nome}_total_ionization_cross_section_passo_{passo}.txt", "w") as resultado:
    for i in range (len(total_cross_section)):
        resultado.write(f'{energia_BEB[i]:.2f}   {total_cross_section[i]}\n')
            

# Aqui iniciaremos o processo de cálculo das seções de choque parciais de ionização (SCPI). Calculando tal quantidade para todos os fragmentos com BR disponíveis.
    # * Todas as quantidades mBEB terão algum indicativo no nome (mBEB ou parcial) *

soma_SCPIs = 0
if controle == '1':
    # A lista 'gamma' reunirá, ao fim dos cálculos, todos os valores do coeficiente gamma, calculados.
    gamma = []
    # Aqui iremos realizar os cálculos para cada fragmento.
    for k in range (len(razao_MQ)):
    # A variável 'Q_prime_70eV' é de extrema importância para o cálculo mBEB.
        Q_prime_70eV = 0
        # A lista 'parcial_cross_section' representa a seção de choque parcial de ionização (SCPI) de um fragmento para uma dada energia.
        parcial_cross_section = []
        # A lista 'energia_mBEB' contém as energias de elétrons incidentes aos quais iremos calcular as SCPI's.
        Q_prime = []
        # A lista 'Q_prime' representa a quantidade que é calculada pelo mBEB, que está relacionada ao SCPI.
        energia_mBEB = []
        # E representa a energia do elétron incidente.
        E = 0.0
        EA = energia_aparecimento[k]
        print(EA)
        # Note que que optei por, em cada razão MQ eu opto por zerar as quantidades relacionadas a energia e SCPI transformando-as em listas vazias.
            # Isto garante a eliminação de quaisquer valores associadas a outro fragmento calculado anteriormente.

        # Neste while, iremos fazer o cálculo das quantidades Q' (Q_prime), advinda do método mBEB, até a energia de 10 KeV.
        gamma_k = 0.0
        while E <= 10000:
        # Aqui, vamos procurar as contribuições de cada orbital para as SCPI's.
        # Já neste for, j representa o j-ésimo orbital.
            Q = 0
            for j in range (len(potencial)):
                Q_orbital_j = 0
                # Notavelmente, se o elétron incidente tem energia 0, a seção de choque é nula. De fato, elétrons devem ter energia ao menos igual a energia de aparecimento para haver a probabilidade de gerar o fragmento.
                # Assim, temos que levar em considerações apenas orbitais com energias iguais ou superiores a energia de aparecimento de cada íon.
                
                if EA >= potencial[j]:
                    B = EA
                else:
                    B = potencial[j]
                Delta = EA - EI
                # E para haver produção do íon, a energia do elétron incidente tem que ser maior ou igual a energia de aparecimento.
                t_mBEB = E/B
                if Delta >= 0.00: 
                    # Note ainda que se a energia do elétron incidente for exatamente igual a energia de aparecimento temos que t = 1 e ln t = 0, assim pelo método BEB e mBEB esta contribuição será nula.
                    if t_mBEB > 1.0:
                        t_mBEB = E/B
                        # Aqui, finalmente, prosseguimos com o processo de definir variáveis relativas a energia cinética média "reduzida" de tal orbital (u) e a constante S para determinar a contribuição de tal orbital para SCPI.
                        U = cinetica[j]
                        u = U/B
                        S = 8*pi*pow(a,2)*pow(R/B,2)
                        # Calculando a SCPI (mBEB): *Utilizaremos a equação simplificada (Q=1)*.
                        # Separando os termos da fórmula:
                        # 1° termo:
                        term1 = (log(t_mBEB)/2)*(1-pow(t_mBEB,-2))
                        # 2° termo:
                        term2 = 1-1/t_mBEB
                        # 3° termo:
                        term3 = -(log(t_mBEB)/(t_mBEB+1))
                        # Seção de choque do j-ésimo orbital para esta energia i:
                        Q_orbital_j = (S/(1+t_mBEB+u))*(term1 + term2 + term3)
                    Q += Q_orbital_j
                # Neste 'for' somamos a seção de choque proveniente de cada orbital para encontrar a seção de choque total para a energia i.
            Q_prime.append(Q)
            energia_mBEB.append(E)
            # Salvando o outro termo relevante para o método mBEB. Determiando o valor do fator gamma. Chamado aqui do fator gamma.
            if isclose(E, 70.0):
                Q_prime_70eV = Q
                gamma_k = (BR[k]*Q_total_70eV)/Q_prime_70eV
                print(f'Q_prime_70 eV (fragmento com razão massa carga {razao_MQ[k]}): ', Q_prime_70eV)
                gamma.append(gamma_k)
            E += passo
        # Aqui terminamos o cálculo das quantidades provenientes do método mBEB. Então agora devemos calcular o fator gamma para cada fragmento e posteriormente calcular a SCPI de cada fragmento.
    # Agora, com o fator gama definido para o fragmento, podemos finalmente calcular a SCPI do fragmento para todas as energias.
        for c in range (len(Q_prime)):
            SCPI = gamma_k*Q_prime[c]
            parcial_cross_section.append(SCPI)
            # Aqui quero escrever o valor da seção de choque a 70 eV.
            if isclose(energia_mBEB[c], 70.0):
                print(f'A SCPI a 70 eV do fragmento com razão massa/carga {razao_MQ[k]} é {SCPI}.')
                soma_SCPIs += SCPI
    # Por fim, terminamos os cálculos da SCPI

    # Criando arquivo txt com as SCPI para todas as energias para um fragmento.
        print(f'criando o arquivo para razão massa/carga: {razao_MQ[k]}')
        with open(f"{nome}_parcial_ionization_cross_section_razao_MQ_{razao_MQ[k]}.txt", "w") as resultado:
            for i in range (len(parcial_cross_section)):
                resultado.write(f'{energia_mBEB[i]:.2f}   {parcial_cross_section[i]}\n')

# Criando o arquivo txt com os fatores gamma dos fragmentos. 
print(f'Criando o arquivo com o fator gamma para todos os fragmentos.')
with open(f"{nome}_fatorGAMMA.txt", "w") as gamma_factor:
    for l in range (len(razao_MQ)):
        gamma_factor.write(f'{razao_MQ[l]}   {gamma[l]}\n')

# Vou mostrar a razão da SCTI e soma das SCPI de todos os fragmentos.
print(f'A razão de Soma_SCPI(70eV) por Q_total(70eV) é: {soma_SCPIs/Q_total_70eV}. ')

# Sinalização do fim do programa
print('Fim!')