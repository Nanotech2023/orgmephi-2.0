import { Component, OnInit } from '@angular/core'


@Component( {
    selector: 'app-video-container',
    templateUrl: './video-container.component.html',
    styleUrls: [ './video-container.component.scss' ]
} )
export class VideoContainerComponent implements OnInit
{
    showVideo: boolean = false

    constructor() { }

    ngOnInit(): void
    {
    }

    onMouseOver()
    {
        this.showVideo = true
    }

    onMouseOut()
    {
        this.showVideo = false
    }
}
