package img2scan.controller;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class WebApplicationController {

    @GetMapping(value = "/upload")
    public String uploadPage() {
        return "uploadPage";
    }
}
