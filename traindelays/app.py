import streamlit as st
from st_pages import Page, show_pages
import os
import numpy as np
import pandas as pd
import datetime
from params import *
import utils as u
from dotenv import load_dotenv
load_dotenv('.env')

# Set the page configuration
st.set_page_config(
    page_title="Train Delays",
    page_icon=":train:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Page title and intro
box_style = "border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); padding: 20px; background-color: #F0F2F6;"
st.markdown(f"""
    <div style="{box_style}">
        <h1 style="font-family: 'Noto Sans', sans-serif; color: black; font-size: 36px; text-align: center;">
            How long will a train be delayed?
        </h1>
        <p style="font-family: 'Noto Sans', sans-serif; color: black; font-size: 18px; text-align: center; line-height: 1.5;">
            Stay on track with network operations! This dashboard offers real-time insights into train delays, empowering rail operators to anticipate and assess expected delays.
        </p>
    </div>
""", unsafe_allow_html=True)

# Add some space between elements using st.text and '\n' for a line break
st.text('\n')

# Form for input
responsible_manager_list = ('METK', 'ZQBG', 'TEKX', 'QQHP', 'REKE', 'TEKN', 'CQHX', 'MEKO',
       'QQA0', 'IQHP', 'MEKI', 'OQBJ', 'TEKE', 'XQHM', 'MEKP', 'FDBF',
       'QQMH', 'IQHN', 'TXCA', 'IQNE', 'MEKF', 'CQHF', 'IQH1', 'XQCW',
       'IQM1', 'CQHG', 'MDBI', 'OQBG', 'TEKJ', 'XQBV', 'VEK1', 'VEKA',
       'TEKS', 'CQHL', 'UETF', 'REKG', 'MEKK', 'CQHU', 'QQN3', 'MEKJ',
       'IQM2', 'TEKW', 'IQHA', 'ZQMD', 'QQAH', 'AWAJ', 'IQCX', 'IQBF',
       'OQBS', 'AWAS', 'QQBH', 'OQHT', 'OQBT', 'CQHH', 'DEKA', 'IQH2',
       'TEKC', 'ZQBA', 'TXEA', 'IEKA', 'REKN', 'MEJ9', 'XQMD', 'REKS',
       'TEKD', 'MXCA', 'REBK', 'METY', 'FDBH', 'MWAS', 'MDBF', 'REK9',
       'FWAS', 'IQCZ', 'UETD', 'IQHW', 'QQH9', 'FPEI', 'IQAH', 'IQHC',
       'MEBK', 'XEKA', 'ZQHO', 'MEB5', 'IQHH', 'QQFY', 'ZQHU', 'SETG',
       'XQNA', 'IQRE', 'FRGI', 'UETV', 'QQBA', 'TEKR', 'IQBH', 'QEKA',
       'FWAJ', 'VHUC', 'IQNA', 'TEJ5', 'ZQNB', 'QQHC', 'OEKA', 'ZQRD',
       'MEKL', 'MEB1', 'UETB', 'FPET', 'MESA', 'OQCM', 'MEKA', 'UETC',
       'QQBG', 'ADBF', 'QQAN', 'DEBA', 'CQNL', 'CQHK', 'IQVR', 'TEJ4',
       'MPHA', 'FPEC', 'OQBY', 'QQAK', 'UETA', 'ARGI', 'MEJJ', 'TET7',
       'IQNT', 'OQBU', 'TETZ', 'IQDR', 'QQHH', 'VEB9', 'TEJ6', 'OQHU',
       'MEJI', 'METR', 'TETA', 'IQDZ', 'DWAM', 'TEBS', 'QQAA', 'XQIA',
       'IQGF', 'IQFK', 'EET0', 'DEXB', 'MET0', 'OQBL', 'DETU', 'QQBO',
       'DHFA', 'DDBH', 'OQBM', 'IQHT', 'ZQRA', 'CQHJ', 'MRGY', 'MEBJ',
       'IQFM', 'UETU', 'CQND', 'MDBH', 'TEKP', 'APEC', 'TETO', 'ZQHM',
       'IQRM', 'AXHA', 'CQRL', 'METX', 'TEKA', 'IQEW', 'TET8', 'IQEB',
       'APEA', 'SETC', 'IQM3', 'FWAW', 'METW', 'OQBC', 'METU', 'DEHA',
       'REKA', 'FPHA', 'METV', 'ADBH', 'ZQIB', 'DDBF', 'MEBM', 'OQMB',
       'TEJB', 'MEKM', 'RHTA', 'REJ9', 'MXHA', 'XQRA', 'MRZY', 'TEBB',
       'MPEI', 'APET', 'MEK0', 'MEXP', 'THUP', 'DHTA', 'MEBN', 'MHUR',
       'IQHM', 'MEK1', 'MEB2', 'VETQ', 'DETG', 'VXCA', 'MET3', 'IQMA',
       'MET9', 'CQHB', 'REB7', 'XQVD', 'QQBY', 'QQNY', 'DPEC', 'MEFC',
       'MHUS', 'OQKL', 'TEBJ', 'TEXX', 'IQBG', 'FWAM', 'QQRF', 'QQRY',
       'MPET', 'MWAW', 'TEKZ', 'TEKO', 'QQDD', 'OQD1', 'ZQMB', 'VEK2',
       'OQBF', 'IQAG', 'THTG', 'OQBV', 'ZQBN', 'ZQHT', 'UETM', 'OQMW',
       'MEBP', 'VHYU', 'IQA7', 'REB4', 'MEK4', 'QQAJ', 'CQHP', 'IQRA',
       'IQR1', 'TEBI', 'UETJ', 'MEJN', 'OQMF', 'IQGR', 'OQNV', 'MPES',
       'CQRD', 'MEJG', 'ZQBD', 'REB2', 'TEBM', 'SETH', 'IQI8', 'VEB3',
       'MEK3', 'MHU3', 'MWAJ', 'VEJ8', 'VHU5', 'QQNU', 'QQR3', 'IQR5',
       'MWAE', 'IQA1', 'OQD2', 'MPEC', 'QQHO', 'TEBT', 'MEK2', 'THUZ',
       'MEBX', 'ZQCY', 'MEJ2', 'TEBK', 'APEP', 'APOF', 'MRGI', 'FDBI',
       'MEKN', 'MEKQ', 'MHTB', 'QQDJ', 'THYT', 'RXCA', 'FXHA', 'VHFU',
       'MEBV', 'VHU7', 'UETE', 'SETE', 'SETF', 'APES', 'FRGF', 'DWAS',
       'VEBH', 'MPAA', 'OQBD', 'MEFP', 'FRTA', 'SETB', 'RHTB', 'MEJ8',
       'THF1', 'VEB4', 'IQCS', 'OQHV', 'QQHE', 'IQCA', 'VHFK', 'VEJ3',
       'TEKT', 'OQHX', 'MPOF', 'AWAW', 'MEBZ', 'OQBK', 'MEXB', 'FPOF',
       'MEBD', 'OQBR', 'TEB3', 'TETF', 'DED4', 'IQDB', 'TET4', 'FWAE',
       'XQFM', 'XQGL', 'MEFO', 'MHY6', 'QQAP', 'QQD6', 'DPET', 'OQBN',
       'IQR3', 'VEB1', 'ZQRB', 'TEJ2', 'XQWC', 'XQGD', 'TEB9', 'OQDI',
       'DETK', 'IQRK', 'IQV9', 'FPES', 'THF3', 'IQDD', 'THTC', 'THYA',
       'IQWS', 'VHFW', 'SETA', 'REBL', 'OQCL', 'TETN', 'TPAA', 'FRZY',
       'MHU1', 'OQCZ', 'QQMN', 'IQBS', 'XQDZ', 'MHF7', 'CQEW', 'OQMR',
       'QQJA', 'ZQNY', 'MET2', 'TEXA', 'EET6', 'TETL', 'VEB7', 'THTR',
       'QQHN', 'DEJL', 'MRTA', 'OQKF', 'IQGL', 'OQIQ', 'MXEA', 'MHBA',
       'TET9', 'MEB3', 'OQD7', 'METG', 'TEBD', 'VEB5', 'UETW', 'THYU',
       'QQDX', 'VEK3', 'IQA0', 'MEJL', 'TEBC', 'OQGY', 'RHU3', 'TEJ1',
       'IQI3', 'MEBL', 'TET5', 'MHF1', 'THTT', 'XQFO', 'VHUL', 'EETA',
       'IQA8', 'IQBR', 'VHUB', 'VHUK', 'TEFC', 'RHUU', 'VHY7', 'OQDS',
       'OQAX', 'IQBW', 'THF4', 'THU1', 'CQNK', 'IQHE', 'MHY2', 'IQND',
       'VETB', 'UETI', 'CQNA', 'VHU1', 'THTM', 'VEBG', 'OQCC', 'RHU2',
       'MEH4', 'OQNY', 'VHUR', 'IQVN', 'QQAM', 'OQRZ', 'TEJX', 'ZQHA',
       'THU5', 'DHYZ', 'MEJ7', 'APEI', 'OQMI', 'OQMC', 'OQD8', 'REBI',
       'VHFZ', 'REB6', 'DEFU', 'IQWC', 'QQCH', 'TET2', 'MEJF', 'VEJH',
       'REBS', 'UETL', 'UETS', 'REBU', 'VHTA', 'RXEA', 'CQHA', 'RETQ',
       'VHUM', 'TEBQ', 'CQET', 'OQCA', 'FPEF', 'ZQDJ', 'DETM', 'OQHA',
       'IQBM', 'VEH6', 'THYM', 'THFO', 'IQIU', 'OQJW', 'MHOA', 'VEXA',
       'AWAM', 'VHUS', 'VHUF', 'IQGN', 'THY6', 'VHU3', 'MEJK', 'TEHF',
       'UETN', 'UET0', 'MRDY', 'ZQDX', 'DED3', 'MEFL', 'MHLG', 'QQMU',
       'MPEA', 'MEBT', 'IQG8', 'CQFC', 'RESA', 'THUN', 'OQCD', 'VHYG',
       'QQG7', 'THUK', 'QQRD', 'FPEA', 'REBO', 'IQCP', 'ZQAI', 'MET8',
       'IQAQ', 'OQCJ', 'VETR', 'IQGU', 'MHYY', 'TESA', 'OQR8', 'VEH5',
       'MXHI', 'TEBG', 'MEB9', 'TEFD', 'VHUU', 'RETT', 'FPEX', 'XQDR',
       'IQV1', 'IQRT', 'OQRV', 'TEDR', 'THTV', 'ZQDB', 'IQFJ', 'MHFP',
       'OQIC', 'IQA3', 'OQKM', 'ZQMA', 'TEB2', 'XQEB', 'THTH', 'THFY',
       'EET2', 'QQJD', 'IQMS', 'TEJ7', 'OQIX', 'IQCD', 'CQLR', 'TETR',
       'IQN1', 'MRHY', 'IQAA', 'OQCG', 'QQAO', 'OQYA', 'QQEY', 'THTA',
       'DHUZ', 'ZQRF', 'THYD', 'MHU4', 'THF8', 'SETR', 'OQDK', 'OQCB',
       'UETX', 'TEBE', 'THUR', 'IQMR', 'IQCC', 'TEXD', 'TPEZ', 'RETU',
       'METJ', 'FQAY', 'THYK', 'DETL', 'OQLM', 'IQMW', 'THUA', 'TEBF',
       'VEB6', 'TETH')
incident_reason_list = ("IB - Points failure (including no fault found)" ,
                        "IP - Points failure caused by snow or frost where heaters are fitted but found to be not turned on, not operative or defective" , "JT - Points failure caused by snow or frost where heaters are not fitted" , "IQ - Trackside sign blown down, fallen over, missing, defective, mis-placed" , "ID - Level crossing faults and failure incl. barrow/foot crossings and crossing treadles" , "JA - TSR speed restrictions for track work outside of the Timetable Planning Rules" , "JS - Condition of Track TSR outside the Timetable Planning Rules" , "IR - Broken/cracked/twisted/buckled/flawed rail" , "IS - Track defects (other than rail defects) inc. fish plates, wet beds etc." , "IT - Rough ride or bumps reported - cause not known or no fault found" , "JB - Reactionary Delay to 'P' coded TSRs" , "IV - Cutting or embankment earthslip, rock fall or subsidence (not the result of severe weather on the day of failure)" , "JD - Structures - Bridges/tunnels/buildings/retaining walls/sea defences (not bridge strikes)" , "I8 - Animal Strike or Incursion within the control of Network Rail" , "IZ - Other Infrastructure causes" , "J4 - Infrastructure Safety Issue Reported by Member of the Public - No Fault Found" , "J5 - Infrastructure Asset fault reported but proven to be mistaken" , "J9 - Preventative Maintenance to the infrastructure in response to a Remote Condition Monitoring Alert" , "JF - Off track asset defects or issues on the NR network (not due to vandalism or weather or part of station infrastructure)" , "JX - Miscellaneous items on track including litter (not including leaves, result of vandalism, weather or fallen/thrown from trains)" , "I6 - Delays as a result of line blocks / track patrols (including late handback)" , "I5 - Possession over-run from planned work" , "I7 - Engineer's train late into, from or failed in possession" , "J8 - OTM DAMAGE" , "JG - ESR/TSR Work not comp/canx pssn (restriction did not exist prior to pssn)" , "JL - Safety related incident caused by maintenance or infrastructure staff oversight or error (not Operations staff)" , "X2 - Severe flooding beyond that which could be mitigated on Network Rail infrastructure" , "X3 - Lightning Strike - damage to protected systems" , "X9 - Points failure caused by severe snow or ice where heaters are fitted and working as designed" , "XH - Severe heat affecting infrastructure the responsibility of Network Rail (excluding heat related speed restrictions)" , "XT - Severe snow or ice affecting infrastructure which is the responsibility of NR (including implementation of Key Route Strategy)" , "XW - Severe weather not snow affecting infrastructure the responsibility of Network Rail" , "IW - Non severe weather - snow/ice/frost affecting infrastructure equipment excluding points" , "J6 - Lightning strike against unprotected assets" , "JH - Critical Rail Temperature speeds, (other than buckled rails)" , "JK - Flooding not due to exceptional weather" , "OG - Ice on conductor rail/OHLE" , "X4 - Blanket speed restrictions or Key Route Strategy implemented with Group Standards or national operational safety instructions" , "OE - Failure to lay Sandite or operate Railhead Conditioning train as programmed" , "QH - Adhesion problems due to leaf contamination" , "QI - Cautioning due to railhead leaf contamination" , "JP - Failure to maintain vegetation within network boundaries in accordance with prevailing Network Rail standards" , "I9 - Fires starting on Network Rail Infrastructure" , "Q3 - NZ Pumps T" , "I1 - Overhead line/third rail defect" , "I2 - AC/DC trip (including no fault or cause found)" , "I4 - OHLE/third rail power supply failure or reduction" , "IH - Power Supply And Distribution System Failure" , "IA - Signal failure (including no fault found)" , "IC - Track circuit failure (including no fault found)" , "J3 - Axle Counter Failure" , "IE - Signalling Functional Power Supply Failure" , "IF - Train Describer/Panel/ARS/SSI/TDM Remote Control failure" , "IJ - AWS/ATP/TPWS/Train stop/On track equipment failure" , "IN - HABD/Panchex/WILD/Wheelchex fault, failure or mis-detection" , "J2 - Network Rail train dispatch equipment failure (including no fault found but excluding telecoms equipment)" , "IM - Infrastructure Balise Failure (TASS / ETCS / ERTMS)" , "JR - Delay due to RBC issues affecting ETCS / ATO operation (not Balise related)" , "IK - Telecom equipment failure (including no fault found)" , "J0 - Telecom equipment radio failure (GSM-R)" , "II - Signalling lineside cable fault" , "QJ - Special working for leaf-fall track circuit operation" , "XP - BRIDGE HIT" , "XB - Vandalism or theft (including the placing of objects on the line)" , "XR - Cable vandalism or theft" , "XD - Level Crossing Incidents including misuse and emergency services being prioritised over rail services" , "XN - Road or crossing related incidents inc. cars on line, crossing misuse and priority to emergency services (NOT bridge strikes)" , "OA - Regulation Decision Made With Best Endeavours" , "OB - Delayed by signaller not applying applicable regulating policy" , "OC - Signaller including mis-routing (not ERTM /ETCS related)" , "OL - Signal Box not open during booked hours" , "OQ - Incorrect simplifier" , "OR - LOM directive or Signaller correctly applying local instructions (ex late running trains or infrastructure Accepted Limitation)" , "OD - Delays due to National/Regional/Route Operations directives or Route Control decision or directive" , "QN - VSTP Schedule/ VSTP Process (TSI created schedule)" , "OM - Technical failure associated with a Railhead conditioning train" , "OS - Late start or delays to Railhead Conditioning or Ghost Train due to its own activity and not in reaction to another incident" , "OH - ARS / TMS / SARS software problem (excluding scheduling issues and technical failures)" , "OJ - Fire in station building/platform affecting operators not booked to call at that stations" , "OK - Delay caused by Operating staff oversight, issues or absence (excluding signallers and Control)" , "OT - Ops Safety TSR implemented for sighting issues relating to foot crossings, level crossings or signals (Not vegetation caused)" , "OV - Fire or evacuation due to fire alarm of Network Rail buildings other than stations not due to vandalism" , "OZ - Other Network Rail operating causes" , "QA - WTT schedule and or LTP Process including erroneous simplifiers" , "QB - Planned engineering work - diversion/SLW not timetabled (outside the Timetable Planning Rules)" , "QM - Train schedule/STP Process including erroneous simplifiers" , "Q1 - Takeback Pumps" , "QT - Delay accepted by Network Rail as part of commercial agreement where no substansive delay reason is identified" , "XA - Trespass (including non-intentional)" , "XC - Fatalities or injuries caused by being hit by train (including non-intentional)" , "XF - Police searching the line" , "XI - Security alert affecting the Network Rail network (incl. line blocks for emergency services attending off network incidents)" , "XL - Fire external to but directly affecting the network (incl. line blocks for emergency services attending off network incidents)" , "X8 - Animal Strike or incursion not within the control of Network Rail" , "XK - National Grid Power Failure - local area also affected (inc outage, surges, blips where working standby generator/UPS installed)" , "XM - External utility incident including gas, water mains, overhead power lines" , "XO - External trees, building or structures encroaching or falling onto network infrastructure (not weather or vandalism)" , "XU - Sunlight on signal or dispatch equipment Where all responsible mitigation has been taken" , "XV - Fire or evacuation due to fire alarm of Network Rail buildings due to vandalism (not including stations)" , "ZS - No Cause ascertainable for a Sub-Threshold Delay causing Threshold Reactionary (where agreed by both parties)" , "ZU - No Cause Identified After investigation by both Parties" , "ZY - Univestigated station overtime System Roll-up Only" , "ZZ - Unexplained loss in running system Roll-up Only" , "ON - Delays not properly investigated by Network Rail" , "OU - Delays not Investigated by Network Rail" , "MS - Planned underpowered or shortformed service and or vehicle, incl. exam set swaps" , "MU - Depot operating problem" , "FH - FOC Planning issue (not diagramming or rostering)" , "FJ - FOC Control decision or directive including diversion requests and errors" , "FK - Train diverted/re-routed at FOC request" , "FO - Time Lost en-route believed to be operator cause and information required from Operator (Ops Responsibility)" , "FX - Freight train running at lower class or speed than planned classification or overweight" , "FZ - Other FOC causes incl. cause to be specified, including mishaps" , "RD - Attaching/detaching/shunter/watering" , "RL - Special Stop Orders - authorised by TOC Control (including any delay at point of issue)" , "T8 - Delays at Station believed to be operator cause and Information required from operator (Ops responsibility)" , "TA - Train-crew/loco/stock/unit diagram issues" , "TB - Train cancelled or delayed at Train Operators request" , "TO - Time lost en-route believed to be Operator cause and information required form operatore (Ops Responsibility)" , "TP - Special Stop Orders" , "TR - Train Operating Company Directive" , "TX - Delays incurred on non-Network Rail running lines or networks including London Underground (except fleet related delays)" , "TY - Mishap-Train Operating Company cause" , "TZ - Other Passenger Train Operating Company causes" , "FC - Freight Train Driver error, SPAD, Wrong routing or Missed AWS/DSD [No change]" , "FE - Train Crew not available including after rest" , "FF - FOC Diagramming or Rostering issue" , "FG - Driver adhering to company professional driving standards or policy" , "T3 - Waiting connections from other transport modes" , "TG - Driver" , "TH - (Senior) Conductor/Train Manager" , "TI - Traincrew rostering problem" , "TJ - Tail lamp or headlamp missing, not lit or wrongly displayed" , "TW - Driver adhering to company professional driving standards or policy" , "M0 - Confirmed train cab based safety system fault (including GSMR)" , "M1 - Confirmed Pantograph ADD, associated system faults, positive PANCHEX activations and train borne power switch over systems (AC)" , "M7 - Door and Door system faults" , "M8 - Technical failures above the Solebar" , "M9 - Reported fleet equipment defect - no fault found" , "MB - Electic Loco failure, defect, attention" , "MC - Diesel Loco failure, defect, attention" , "MD - Technical failures below the solebar" , "ME - Steam locomotive failure/defect/attention" , "ML - Wagons, coaches and parcel vehicle faults" , "MN - Brake and brake systems faults; including wheel flats where no other cause had been identified" , "MR - Sanders and scrubber faults" , "MT - Confirmed train borne safety system faults (not cab based)" , "MV - Engineers on-track equipment failure outside possession" , "MW - Weather - effect on T&RS equipment" , "MY - Coupler, Coupler system and Jumper cable faults" , "NA - On train TASS/TILT failure" , "R1 - Station staff dispatch issues including dispatch errors" , "R2 - Late TRTS given by station staff" , "R3 - Station Staff unavailable - missing or uncovered" , "R4 - Station staff split responsibility - unable to cover all duties" , "R5 - Station staff error - e.g wrong announcements misdirection" , "R7 - Station delays as a result of overcrowding due to planned events (e.g. sports fixtures, concerts)" , "R8 - Delay at Station believed to be operator cause and information required from operator (Ops Responsibility)" , "RB - Passengers joining/alighting" , "RC - re-booked assistance for a person with reduced mobility joining/alighting," , "RE - Lift/escalator defect/failure" , "RH - Station evacuated due to fire alarm" , "RI - Waiting connections - not authorised by TOC Control" , "RM - Waiting connections from other transport modes" , "RO - Passengers taken ill on platform" , "RP - Passenger dropped object whilst boarding/alighting from train and train delayed at TOC request" , "RQ - Un-booked assistance for a person with reduced mobility joining/alighting," , "RT - Loading Luggage" , "RU - Locating lost luggage" , "RV - Customer Information system failure" , "RW - Station flooding (incl. issues with drains) not the result of weather, where the water has not emanated from NR infrastructure" , "RX - Station delay due overcrowding due unplanned events or incident (line or station closure) where causal event is not determined" , "RY - Mishap - Station Operating causes" , "RZ - Other Station Operating causes" , "T2 - Delay at unstaffed station to non-DOO train" , "V8 - Train striking or being struck by a bird" , "VA - Disorder/drunks or trespass" , "VB - Vandalism or theft" , "VC - Fatalities and or injuries sustained on platform result of struck by train or falling from a train" , "VD - Passenger taken ill on train" , "VE - Ticket irregularities or refusals to pay" , "VF - Fire caused by vandalism" , "VG - Police searching train" , "VH - Passenger Communication cord, door egress or emergency train alarm operated" , "VI - Security alert affecting stations and depots" , "VW - Severe weather affecting passenger Fleet equipment including follwogin company standards/policies or Rule book instructions" , "VZ - Other passenger or external causes the responsibility of TOC" , "AA - Waiting acceptance into off Network Rail network Terminal or Yard" , "AC - Waiting Train preparation or completion of TOPS list/RT3973" , "AD - Off Network Rail network Terminal or Yard staff shortage including reactionary congestion caused by shortage" , "AE - Congestion in off Network Rail network Terminal or Yard" , "AG - Wagon load incident including adjusting loads or open door" , "AH - Customer or off Network Rail network yard equipment breakdown/reduced capacity" , "AJ - Waiting Customer's traffic including release information and documentation" , "AK - Safety Ins and mishaps(derailments, fire, chemical spill) in off n/w freight yard or terminal (inc private sdgs affecting FOC" , "AX - Failure of off network infrastructure (FOC or private)" , "AZ - Other Freight Operating Company cause, to be specified (including congestion), in off Network Rail network terminals or yards" , "FW - Late start/yard overtime not explained by Operator" , "MP - Rail / wheel interface, adhesion problems (including ice on the running rail)" , "TT - Leaf fall Neutral")
lon_lat_df = u.read_data_from_bq(credentials = os.getenv('SERVICE_ACCOUNT'),
                  gcp_project = os.getenv('GCP_PROJECT_ID'), bq_dataset = os.getenv('BQ_DATASET'),
                  table = os.getenv('GEO_COOORDINATES_TABLE_ID'))
with st.form(key='params_for_api'):
    departure_station = st.selectbox("Departure Station", lon_lat_df['Station_Name'].values)
    arrival_station = st.selectbox("Arrival Station", lon_lat_df['Station_Name'].values)
    departure_date = st.date_input('Departure Date', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    departure_time = st.time_input('Departure Time', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    arrival_date = st.date_input('Arrival Date', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    arrival_time = st.time_input('Arrival Time', value=datetime.datetime(2012, 10, 6, 12, 10, 20))
    type_day = st.selectbox('Day Type',('WD - Weekday', 'SU - Sunday', 'SA - Saturday', 'BH - Bank Holiday'),index=2)
    train_service_group_code = st.selectbox('Train Service Group',('EK01 -- Orbitals','EK02 -- London-Watford (DC lines)',
     'EK03 -- East London Lines', 'EK04 -- West Anglia Inner', 'EK05 -- Romford-Upminster','EK99 -- Miscellaneous '), index=2)
    train_schedule_type = st.selectbox('Train Schedule Type',('LTP','(V)STP Overlay','(V)STP Base','(V)STP Cancellation'),index=2)
    train_unit_class = st.selectbox('Train unit class',('375.0', '378.0', '710.0', '315.0', '317.0','313.0','None'))
    train_manager = st.selectbox('Train Manager',responsible_manager_list,index=2)
    incident_reason = st.selectbox('Incident Reason', incident_reason_list,index = 2)
    reactionary_reason = st.checkbox('Is the delay at the site of the incident?')
    event_code = st.checkbox('Is the delay automatically logged?')
    st.form_submit_button('Predict')

params = dict(departure_station = departure_station,
              arrival_station = arrival_station,
              departure_date = departure_date,
              departure_time = departure_time,
              arrival_date = arrival_date,
              arrival_time = arrival_time,
              type_day = type_day,
              train_service_group_code = train_service_group_code,
              train_schedule_type = train_schedule_type,
              train_unit_class = train_unit_class,
              train_manager = train_manager,
              incident_reason = incident_reason,
              reactionary_reason = reactionary_reason,
              event_code = event_code)

#network_rail_pred_api_url = '...'
#response = requests.get(network_rail_pred_api_url, params=params)
#prediction = response.json()
#pred = prediction['fare']
#st.header(f'Fare amount: ${round(pred, 2)}')

# Specify what pages should be shown in the sidebar, and their titles and icons
show_pages(
    [
        Page("traindelays/app.py", "Home", ":house:"),
        Page("traindelays/interface/pages/About.py", "About us", ":information_source:"),
        Page("traindelays/interface/pages/Data&Methodology.py", "Data & Methodology", ":bar_chart:")
    ]
)
