# parser.py
import json
from collections import defaultdict

def load_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def is_hypergiant_from_star(s):
    # Prioriza campo explícito, si no existe infiere por type
    if 'hypergiant' in s:
        return bool(s.get('hypergiant'))
    typ = s.get('type', '') or ''
    return 'supergiant' in typ.lower() or 'hypergiant' in typ.lower()

def build_global_nodes(data):
    """
    Unifica estrellas por coordenadas (x,y).
    Devuelve:
      nodes: dict gid -> node dict
      id_to_gid: mapping from original star id -> gid
    Node structure:
      {
        "gid": str,
        "coords": (x,y),
        "originals": [orig_id,...],
        "labels": [name,...],
        "constellations": set([...]),
        "hypergiant": bool,
        "meta_list": [star_entry,...]  # copia de entradas originales
      }
    """
    coord_index = {}
    nodes = {}
    id_to_gid = {}
    next_gid = 1
    for const in data.get("constellations", []):
        cname = const.get("name")
        for s in const.get("stars", []):
            x, y = s.get("x"), s.get("y")
            key = (x, y)
            if key not in coord_index:
                gid = f"g{next_gid}"; next_gid += 1
                node = {
                    "gid": gid,
                    "coords": key,
                    "originals": [s.get("id")],
                    "labels": [s.get("name") or s.get("label") or str(s.get("id"))],
                    "constellations": set([cname]),
                    "hypergiant": is_hypergiant_from_star(s),
                    "meta_list": [s.copy()]
                }
                nodes[gid] = node
                coord_index[key] = gid
                id_to_gid[s.get("id")] = gid
            else:
                gid = coord_index[key]
                node = nodes[gid]
                node["originals"].append(s.get("id"))
                node["labels"].append(s.get("name") or s.get("label") or str(s.get("id")))
                node["constellations"].add(cname)
                if is_hypergiant_from_star(s):
                    node["hypergiant"] = True
                node["meta_list"].append(s.copy())
                id_to_gid[s.get("id")] = gid
    return nodes, id_to_gid

def build_edges(data, id_to_gid):
    """
    Reconstruye aristas a partir de data['routes'] que referencian original ids.
    Normaliza a undirected edges entre gid's.
    Cada edge = {"a":gid1,"b":gid2,"distance":..., "danger_level":..., "blocked":False}
    """
    edges_map = {}
    for r in data.get("routes", []):
        f = r.get("from"); t = r.get("to")
        gid_from = id_to_gid.get(f)
        gid_to = id_to_gid.get(t)
        if gid_from is None or gid_to is None:
            # Si una referencia no se mapea, la ignoramos, pero es buena idea avisar al usuario
            continue
        if gid_from == gid_to:
            continue
        key = tuple(sorted((gid_from, gid_to)))
        # keep smallest distance if duplicates
        distance = r.get("distance", 0)
        danger = r.get("danger_level", 0)
        if key not in edges_map or edges_map[key]["distance"] > distance:
            edges_map[key] = {"a": key[0], "b": key[1], "distance": distance, "danger_level": danger, "blocked": False}
    return list(edges_map.values())
