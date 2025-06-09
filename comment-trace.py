# -*- coding: utf-8 -*-
import sys
import os.path
#idaapi.split_sreg_range(instruction_pointer, idaapi.str2reg("T"), required_t_value, idaapi.SR_user)

if __name__ == "__main__":
    trace_path = ""
    filename = ""
    in_ida = True

    try:
        import idc
        in_ida = True
    except ImportError as e:
        print("not run in ida python skip comment...")
        in_ida = False
    #
    is_clean=0
    if (in_ida):
        trace_path = idc.AskFile(0, "*.*", "trace path")
        is_clean = idc.AskLong(0, "clean path?")
        if (not os.path.isabs(trace_path)):
            script_path = os.path.split(os.path.realpath(__file__))[0]
            trace_path = "%s/%s"%(script_path, trace_path)
        #
        filename = idc.get_root_filename()
    #
    else:
        trace_path = sys.argv[1]
        filename = sys.argv[2]
        if (len(sys.argv)<3):
            print("usage %s <trace-file> <filename>"%sys.argv[0])
            sys.exit(-1)
        #
    #
    dic_call = {}
    with open(trace_path) as f:
        for line in f:
            line = line.strip()
            if (line == ""):
                continue
            #
            if (line.find(filename)<0):
                continue
            #
            sa = line.split(":")
            start = sa[0].rfind("]")+1
            addr = sa[0][start:]
            count = 1
            if (addr in dic_call):
                count = dic_call[addr] + 1
            dic_call[addr] = count
        #
    #
    print(dic_call)
    if (in_ida):
        for addr in dic_call:
            comm = ""
            color = 0xFFFFFF 
            int_addr = int(addr, 16)
            if is_clean == 0:
                int_call = dic_call[addr]
                comm = str(int_call)
                if (int_call > 0 and int_call < 20):
                    color = 0xFFAFFF
                #
                elif (int_call >=20 and int_call < 40):
                    color = 0xFF7FFF
                else:
                    color = 0xFF00FF
                #
            #
            idc.MakeComm(int_addr, comm)
            idc.SetColor(int_addr, idc.CIC_ITEM, color)
        #
    #
#
