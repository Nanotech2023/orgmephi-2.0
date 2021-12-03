import { Component } from '@angular/core'


@Component( {
    selector: 'app-video-container',
    templateUrl: './video-container.component.html',
    styleUrls: [ './video-container.component.scss' ]
} )
export class VideoContainerComponent
{
    videoSrc: string

    constructor()
    {
        const videoArray: string[] = [
            "/assets/gifs/cryst_2_compr.gif",
            "/assets/gifs/Displace_2_compr.gif",
            "/assets/gifs/electro_2_compr.gif",
            "/assets/gifs/light-2_compr.gif",
            "/assets/gifs/metaballs_2_compr.gif",
            "/assets/gifs/spline_ball_2.gif",
            "/assets/gifs/trails_v02_compr.gif"
        ]
        this.videoSrc = videoArray[ Math.floor( Math.random() * videoArray.length ) ]
    }
}
