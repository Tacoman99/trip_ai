import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Clock, User, Tag, MapPin, Search, Layers } from "lucide-react"
import { useEffect, useRef, useState } from "react"

export default function GoogleMapCard(props) {
  const mapRef = useRef(null);
  const [mapLoaded, setMapLoaded] = useState(false);
  
  // Load the Google Maps JavaScript API
  useEffect(() => {
    if (window.google?.maps?.importLibrary) {
      setMapLoaded(true);
      return;
    }
    
    // Define the loader function - this is the minified loader from Google
    const loadGoogleMapsApi = () => {
      window.googleMapsApiLoading = true;
      const g = {
        key: props.apiKey || "Api-key", // Replace with your API key or pass it as a prop
        v: "weekly"
      };
      
      var h,a,k,p="The Google Maps JavaScript API",c="google",l="importLibrary",q="__ib__",m=document,b=window;
      b=b[c]||(b[c]={});var d=b.maps||(b.maps={}),r=new Set,e=new URLSearchParams;
      const u=()=>h||(h=new Promise(async(f,n)=>{
        await (a=m.createElement("script"));
        e.set("libraries",[...r]+"");
        for(k in g)e.set(k.replace(/[A-Z]/g,t=>"_"+t[0].toLowerCase()),g[k]);
        e.set("callback",c+".maps."+q);
        a.src=`https://maps.${c}apis.com/maps/api/js?`+e;
        d[q]=f;
        a.onerror=()=>h=n(Error(p+" could not load."));
        a.nonce=m.querySelector("script[nonce]")?.nonce||"";
        m.head.append(a);
      }));
      
      d[l]?console.warn(p+" only loads once. Ignoring:",g):d[l]=(f,...n)=>r.add(f)&&u().then(()=>d[l](f,...n));
      
      // Return a promise that resolves when the API is loaded
      return new Promise((resolve) => {
        const checkIfLoaded = setInterval(() => {
          if (window.google?.maps?.importLibrary) {
            clearInterval(checkIfLoaded);
            setMapLoaded(true);
            resolve();
          }
        }, 100);
      });
    };

    // Load the API
    loadGoogleMapsApi();
  }, [props.apiKey]);

  // Initialize the map once the API is loaded
  useEffect(() => {
    if (!mapLoaded || !mapRef.current) return;

    async function initMap() {
      // The location (default to Uluru if not provided)
      const position = props.position || { lat: [-25.344, -25.344], lng: [131.031, 131.031] };
      
      // Request needed libraries
      const { Map } = await google.maps.importLibrary("maps");
      const { AdvancedMarkerElement } = await google.maps.importLibrary("marker");

      // The map, centered at the specified position
      const map = new Map(mapRef.current, {
        zoom: props.zoom || 4,
        center: position,
        mapId: props.mapId || "DEMO_MAP_ID",
      });

      // The marker, positioned at the specified position
      if (props.showMarker !== false) {
        const marker = new AdvancedMarkerElement({
          map: map,
          position: position,
          title: props.markerTitle || "Location",
        });
      }
    }

    initMap();
  }, [mapLoaded, props.position, props.zoom, props.mapId, props.markerTitle, props.showMarker]);

  return (
    <Card className="w-full max-w-md">
      <CardHeader className="pb-2">
        <div className="flex justify-between items-center">
          <CardTitle className="text-lg font-medium">
            {props.title || 'Location Map'}
          </CardTitle>
          <Badge variant="outline">
            {props.locationName || 'Unknown Location'}
          </Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {/* Map container */}
          <div 
            id="map"
            ref={mapRef} 
            className="h-64 w-full rounded-md border"
            style={{ minHeight: "250px" }}
          >
            {!mapLoaded && <div className="flex items-center justify-center h-full">Loading map...</div>}
          </div>
          
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div className="flex items-center gap-2">
              <MapPin className="h-4 w-4 opacity-70" />
              <span>{props.locationName || 'Unnamed location'}</span>
            </div>
            <div className="flex items-center gap-2">
              <Search className="h-4 w-4 opacity-70" />
              <span>Zoom: {props.zoom || 4}</span>
            </div>
            <div className="flex items-center gap-2 col-span-2">
              <Layers className="h-4 w-4 opacity-70" />
              <span>{props.description || 'No description'}</span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}